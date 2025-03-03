import sqlite3
import random

def calculate_tax_percentage_and_average(user_tax):
    conn = sqlite3.connect('cars.db')
    curs = conn.cursor()

    # Query to fetch all the car details
    curs.execute(''' 
        SELECT MARK, MUDEL, ESMANE_REG, MOOTORI_VOIMSUS, KYTUSE_TYYP, AUTOMAKS, REGTASU
        FROM Car
    ''')

    # Fetch all results
    cars = curs.fetchall()

    # Calculate the total number of cars
    total_cars = len(cars)

    # Calculate the average car tax (AUTOMAKS)
    if total_cars > 0:
        total_automaks = sum(car[5] for car in cars)
        average_automaks = total_automaks / total_cars

        # Calculate the percentage of cars with higher and lower tax
        higher_tax_count = sum(1 for car in cars if car[5] > user_tax)
        lower_tax_count = sum(1 for car in cars if car[5] < user_tax)

        higher_percentage = (higher_tax_count / total_cars) * 100
        lower_percentage = (lower_tax_count / total_cars) * 100

        # Filter cars with tax difference of <= 10 EUR from the user's desired tax
        example_cars = [car for car in cars if abs(car[5] - user_tax) <= 10]

        # Sort the example cars based on how close their tax is to the user's provided tax
        example_cars_sorted = sorted(example_cars, key=lambda car: abs(car[5] - user_tax))

        # Remove duplicate mark/model combinations
        seen = set()
        unique_example_cars = []
        for car in example_cars_sorted:
            mark_model = (car[0], car[1])  # (MARK, MUDEL) tuple
            if mark_model not in seen:
                unique_example_cars.append(car)
                seen.add(mark_model)

        # Limit to 3 example cars
        random_example_cars = unique_example_cars[:3]  # Only take the top 3 closest matches

        # Return the results
        return round(higher_percentage, 2), higher_tax_count, round(lower_percentage, 2), lower_tax_count, round(average_automaks, 2), random_example_cars
    else:
        return 0, 0, 0, 0, 0, []  # If there are no cars in the database

def display_car_details(cars):
    # Print each car's details on a new line with aligned columns
    for car in cars:
        mark, model, reg, power, fuel, automaks, regtasu = car
        print(f"🚗 {mark: <12}{model: <15} | 📅 Registreeritud: {reg: <10} | ⚡ Võimsus: {power: <6}kW | ⛽ Kütus: {fuel: <7} | 💰 Aastamaks: {automaks: <8.2f}€ | 🏷️ Registreerimistasu: {regtasu: <8.2f}€")

def display_slider(user_tax, average_automaks):
    # Set the range of the slider (e.g., between 0 EUR and max possible car tax)
    max_tax = 1000  # Max possible car tax (this can be adjusted based on your data)
    min_tax = 0  # Min possible car tax
    slider_length = 50  # Length of the slider

    # Calculate the position of the user's tax and average tax
    user_position = int((user_tax / max_tax) * slider_length)
    average_position = int((average_automaks / max_tax) * slider_length)

    # Build the slider
    slider = ['='] * slider_length
    # Set the color for different regions: Green (left), Yellow (middle), Red (right)
    for i in range(slider_length):
        if i < slider_length // 3:
            slider[i] = '='  # Green section
        elif i < 2 * slider_length // 3:
            slider[i] = '-'  # Yellow section
        else:
            slider[i] = '*'  # Red section

    # Display the slider
    slider_string = ''.join(slider)

    # Display the slider with user tax and average tax markers
    slider_with_markers = slider_string
    slider_with_markers = slider_with_markers[:user_position] + '|' + slider_with_markers[user_position+1:]
    slider_with_markers = slider_with_markers[:average_position] + 'O' + slider_with_markers[average_position+1:]

    # Print the slider
    print(f"\nAastamaksu liugur (0 EUR - 1000 EUR):")
    print(f"[{slider_with_markers}]")
    print(f"  {'User Tax'}: {user_tax:.2f} EUR   {'Average Tax'}: {average_automaks:.2f} EUR")

if __name__ == '__main__':
    try:
        # Ask the user to input their desired car tax
        user_tax = float(input('Sisesta oma soovitud aastamaks: '))
        
        # Call the function to calculate the percentage of cars with higher and lower tax, and the average tax
        higher_percentage, higher_tax_count, lower_percentage, lower_tax_count, average_automaks, random_example_cars = calculate_tax_percentage_and_average(user_tax)
        
        if higher_percentage > 0 or lower_percentage > 0:
            print(f'{higher_percentage}% ({higher_tax_count} autot) autodest on suurem aastamaks kui sinu soovitud maksumus.')
            print(f'{lower_percentage}% ({lower_tax_count} autot) autodest on väiksem aastamaks kui sinu soovitud maksumus.')
        
        if average_automaks > 0:
            if user_tax < average_automaks:
                print(f'Sinu soovitud aastamaks ({user_tax} EUR) on madalam kui keskmine aastamaks ({average_automaks} EUR).')
            else:
                print(f'Sinu soovitud aastamaks ({user_tax} EUR) on suurem või võrdne keskmise aastamaksuga ({average_automaks} EUR).')
        
        # Display the example cars within the tax difference of 10 EUR
        if random_example_cars:
            print("\nNäited autodest, sarnase automaksuga:")
            display_car_details(random_example_cars)
        else:
            print("\nEi leitud autosid, mille aastamaks oleks sinu soovitud maksumusega ±10 EUR.")
        
        # Display the green-to-red slider with the user and average tax
        display_slider(user_tax, average_automaks)
        
    except ValueError:
        print("Palun sisesta korrektne number aastamaksu jaoks.")
