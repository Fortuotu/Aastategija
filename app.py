from flask import Flask, render_template, request, jsonify
import sqlite3
import random
import folium

app = Flask(__name__)

session = {}
correct_car = {}

@app.route('/')
def index():
    return render_template('index.html')

def get_random_cars():
    # Connect to the database
    conn = sqlite3.connect('cars.db')
    curs = conn.cursor()

    # Query to select two random cars
    curs.execute('''
        SELECT MARK, MUDEL, ESMANE_REG, MOOTORI_VOIMSUS, MOOTORI_MAHT, TAISMASS, KYTUSE_TYYP, KERE_NIMETUS, AUTOMAKS, REGTASU
        FROM Car
        ORDER BY RANDOM()
        LIMIT 2
    ''')

    # Fetch the two random cars
    cars = curs.fetchall()
    conn.close()

    # If there are two cars, format them and return as a JSON response
    if len(cars) == 2:
        car1 = cars[0]
        car2 = cars[1]

        cars_dict = {
            'car1': {
                'mark': car1[0],
                'model': car1[1],
                'reg': car1[2],
                'power': car1[3],
                'engine_capacity': car1[4],
                'weight': car1[5],
                'fuel': car1[6],
                'body': car1[7],
                'tax': car1[8],
                'registration_fee': car1[9],
            },
            'car2': {
                'mark': car2[0],
                'model': car2[1],
                'reg': car2[2],
                'power': car2[3],
                'engine_capacity': car2[4],
                'weight': car2[5],
                'fuel': car2[6],
                'body': car2[7],
                'tax': car2[8],
                'registration_fee': car2[9],
            }
        }

        global correct_car
        correct_car = cars_dict[random.choice(('car1', 'car2'))]

        global session
        session = cars_dict

        return jsonify(cars_dict)
    
    return jsonify({})

@app.route('/game', methods=['GET'])
def game():
    return render_template('game.html')

@app.route('/guess', methods=['POST'])
def guess():
    car_guess = request.form.get('car_guess')
    
    ret_val = 'Wrong answer.'

    if (session[f'car{car_guess}']['tax'] == correct_car['tax'] and session[f'car{car_guess}']['registration_fee'] == correct_car['registration_fee']):
        ret_val = 'Correct!'

    return ret_val

@app.route('/get_random_cars', methods=['GET'])
def get_random_cars_route():
    return get_random_cars()

# Andmebaasi ühendus
def get_db_connection():
    conn = sqlite3.connect("cars.db")
    conn.row_factory = sqlite3.Row  # Võimaldab sõnastikulaadseid tulemusi
    return conn

@app.route("/mudelid", methods=["GET", "POST"])
def mudelid():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Vali unikaalsed margid
    cursor.execute("SELECT DISTINCT MARK FROM Car")
    marks = [row["MARK"] for row in cursor.fetchall()]

    selected_mark = request.form.get("mark")
    selected_model = request.form.get("model")

    models = []
    stats = None
    cars = []
    total_count = 0  # Kokku vasteid
    mark_model_count = 0  # Kui paljudel autodel on see mark ja mudel

    if selected_mark:
        cursor.execute("SELECT DISTINCT MUDEL FROM Car WHERE MARK = ?", (selected_mark,))
        models = [row["MUDEL"] for row in cursor.fetchall()]

        if selected_model:
            cursor.execute(
                """SELECT ESMANE_REG, MOOTORI_VOIMSUS, MOOTORI_MAHT, KYTUSE_TYYP, KERE_NIMETUS, AUTOMAKS, REGTASU
                FROM Car WHERE MARK = ? AND MUDEL = ?""",
                (selected_mark, selected_model),
            )
            all_cars = cursor.fetchall()  # Kõik vastavad autod
            total_count = len(all_cars)  # Kokku vasteid andmebaasis

            if all_cars:
                automaksud = [float(car["AUTOMAKS"]) for car in all_cars]
                reg_tasud = [float(car["REGTASU"]) for car in all_cars]

                stats = {
                    "avg_tax": sum(automaksud) / len(automaksud),
                    "min_tax": min(automaksud),
                    "max_tax": max(automaksud),
                    "avg_reg": sum(reg_tasud) / len(reg_tasud),
                    "min_reg": min(reg_tasud),
                    "max_reg": max(reg_tasud),
                }

                cars = all_cars[:21]  # Kuvame ainult 20 autot

            # Arvuta, kui paljudel autodel on see mark ja mudel
            cursor.execute("SELECT COUNT(*) FROM Car WHERE MARK = ? AND MUDEL = ?", (selected_mark, selected_model))
            mark_model_count = cursor.fetchone()[0]

    conn.close()
    return render_template(
        "mudelid.html",
        marks=marks,
        models=models,
        selected_mark=selected_mark,
        selected_model=selected_model,
        stats=stats,
        cars=cars,
        total_count=total_count,
        mark_model_count=mark_model_count
    )

def calculate_tax_percentage_and_average(user_tax):
    conn = sqlite3.connect('cars.db')
    curs = conn.cursor()

    curs.execute(''' 
        SELECT MARK, MUDEL, ESMANE_REG, MOOTORI_VOIMSUS, KYTUSE_TYYP, AUTOMAKS, REGTASU
        FROM Car
    ''')
    
    cars = curs.fetchall()
    total_cars = len(cars)
    
    if total_cars > 0:
        total_automaks = sum(car[5] for car in cars)
        average_automaks = total_automaks / total_cars

        higher_tax_count = sum(1 for car in cars if car[5] > user_tax)
        lower_tax_count = sum(1 for car in cars if car[5] < user_tax)

        higher_percentage = (higher_tax_count / total_cars) * 100
        lower_percentage = (lower_tax_count / total_cars) * 100

        example_cars = [car for car in cars if abs(car[5] - user_tax) <= 10]
        example_cars_sorted = sorted(example_cars, key=lambda car: abs(car[5] - user_tax))

        seen = set()
        unique_example_cars = []
        for car in example_cars_sorted:
            mark_model = (car[0], car[1])
            if mark_model not in seen:
                unique_example_cars.append(car)
                seen.add(mark_model)

        random_example_cars = unique_example_cars[:3]

        return round(higher_percentage, 2), higher_tax_count, round(lower_percentage, 2), lower_tax_count, round(average_automaks, 2), random_example_cars
    else:
        return 0, 0, 0, 0, 0, []

@app.route('/analyys')
def analyys():
    return render_template('analyys.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    user_tax = data.get('user_tax')
    
    if user_tax is None:
        return jsonify({'error': 'User tax is required'}), 400
    
    try:
        user_tax = float(user_tax)
    except ValueError:
        return jsonify({'error': 'Invalid tax value'}), 400
    
    results = calculate_tax_percentage_and_average(user_tax)
    
    response = {
        'higher_percentage': results[0],
        'higher_tax_count': results[1],
        'lower_percentage': results[2],
        'lower_tax_count': results[3],
        'average_automaks': results[4],
        'example_cars': [
            {
                'mark': car[0],
                'model': car[1],
                'registration': car[2],
                'power': car[3],
                'fuel': car[4],
                'automaks': car[5],
                'regtasu': car[6]
            }
            for car in results[5]
        ]
    }
    
    return jsonify(response)

def create_map():
    m = folium.Map(location=[50, 10], zoom_start=4)

    # Andmed iga riigi kohta
    tax_data = {
        "Belgium": [50.85, 4.35, 2892],
        "Finland": [60.17, 24.94, 2723],
        "Ireland": [53.35, -6.26, 2438],
        "Austria": [48.21, 16.37, 2409],
        "Denmark": [55.67, 12.56, 2217],
        "Netherlands": [52.37, 4.90, 2160],
        "Germany": [52.52, 13.40, 1764],
        "Italy": [41.90, 12.49, 1727],
        "France": [48.85, 2.35, 1625],
        "Sweden": [59.33, 18.06, 1543],
        "Portugal": [38.72, -9.14, 1290],
        "Greece": [37.98, 23.72, 1264],
        "Spain": [40.42, -3.70, 1148]
    }

    # Lisame iga riigi kaardile
    for country, data in tax_data.items():
        folium.CircleMarker(
            location=[data[0], data[1]],
            radius=data[2] / 1000,  # Suuruse skaleerimine
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.6,
            popup=f"{country}: €{data[2]}"
        ).add_to(m)

    map_path = "car_map.html"
    m.save(map_path)
    return map_path

@app.route('/car_tax_dashboard')
def dashboard():
    map_path = create_map()
    return render_template("car_tax_dashboard.html", map_path=map_path)

if __name__ == '__main__':
    app.run(debug=True, port=7070)
