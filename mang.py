import sqlite3

def main():
    conn = sqlite3.connect('cars.db')
    curs = conn.cursor()

    while True:
        # Query to select two random cars
        curs.execute('''
            SELECT MARK, MUDEL, ESMANE_REG, MOOTORI_VOIMSUS, MOOTORI_MAHT, TAISMASS, KYTUSE_TYYP, KERE_NIMETUS, AUTOMAKS, REGTASU
            FROM Car
            ORDER BY RANDOM()
            LIMIT 2
        ''')

        # Fetch two random cars
        cars = curs.fetchall()

        if len(cars) == 2:
            # Unpack data for both cars
            car1 = cars[0]
            car2 = cars[1]

            # Unpack car 1 data
            mark1, mudel1, reg1, voim1, maht1, kaal1, kytus1, kere1, automaks1, regtasu1 = car1

            # Unpack car 2 data
            mark2, mudel2, reg2, voim2, maht2, kaal2, kytus2, kere2, automaks2, regtasu2 = car2

            # Display both cars' details (without Aastamaks and RegTasu)
            print(f"\n🚗 {mark1} {mudel1}")
            print(f"📅 Registreeritud: {reg1}")
            print(f"⚡ Võimsus: {voim1} kW")
            print(f"🔧 Mootor: {maht1} cm³")
            print(f"⛽ Kütus: {kytus1}")
            print(f"⚖️ Täismass: {kaal1} kg")
            print(f"🏷️ Kere: {kere1}")

            print(f"\n🚗 {mark2} {mudel2}")
            print(f"📅 Registreeritud: {reg2}")
            print(f"⚡ Võimsus: {voim2} kW")
            print(f"🔧 Mootor: {maht2} cm³")
            print(f"⛽ Kütus: {kytus2}")
            print(f"⚖️ Täismass: {kaal2} kg")
            print(f"🏷️ Kere: {kere2}")

            # Ask the user to guess which car corresponds to the given Aastamaks and RegTasu
            print("\nArva, milline auto vastab järgmistele andmetele:")
            print(f"Aastamaks (Auto maks): {automaks1} EUR")
            print(f"Registreerimistasu (Registreerimise tasu): {regtasu1} EUR")

            # Ask the user to choose between car 1 and car 2
            guess = input("Milline auto see on? Kirjuta '1' auto 1 jaoks või '2' auto 2 jaoks: ").strip()

            # Check if the user's guess is correct
            if guess == '1' and (automaks1 == automaks1 and regtasu1 == regtasu1):
                print("Õige! Auto 1 on see, mida otsid.")
            elif guess == '2' and (automaks2 == automaks1 and regtasu2 == regtasu1):
                print("Õige! Auto 2 on see, mida otsid.")
            else:
                print(f"Vale vastus! Õige auto oli: {mark1} {mudel1} ja {mark2} {mudel2}")
        
        # Ask the user if they want to play again or quit
        play_again = input("\nKas soovid mängida veel? (jah/eii): ").strip().lower()
        
        if play_again != 'jah':
            print("Aitäh mängimast! Head aega!")
            break  # Exit the loop and end the game

    conn.close()

if __name__ == '__main__':
    main()
