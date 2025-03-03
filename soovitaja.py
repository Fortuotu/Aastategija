import sqlite3

def main():
    conn = sqlite3.connect('cars.db')
    curs = conn.cursor()

    try:
        maks = float(input('Kui suurt aastamaksu suudad taluda? '))  # Ensure input is a number

        # Query for 🌟 Kõige uuem (Newest car closest to given tax)
        curs.execute("""
            SELECT MARK, MUDEL, ESMANE_REG, MOOTORI_VOIMSUS, KYTUSE_TYYP, AUTOMAKS, REGTASU 
            FROM Car 
            WHERE AUTOMAKS IS NOT NULL 
            ORDER BY ABS(AUTOMAKS - ?), ESMANE_REG DESC 
            LIMIT 1
        """, (maks,))
        newest_car = curs.fetchone()

        # Query for 💪 Kõige võimsam (Most powerful car closest to given tax)
        curs.execute("""
            SELECT MARK, MUDEL, ESMANE_REG, MOOTORI_VOIMSUS, KYTUSE_TYYP, AUTOMAKS, REGTASU 
            FROM Car 
            WHERE AUTOMAKS IS NOT NULL 
            ORDER BY ABS(AUTOMAKS - ?), MOOTORI_VOIMSUS DESC 
            LIMIT 1
        """, (maks,))
        most_powerful = curs.fetchone()

        # Query for 💰 Uus ja soodsam (Newest & most affordable car)
        curs.execute("""
            SELECT MARK, MUDEL, ESMANE_REG, MOOTORI_VOIMSUS, KYTUSE_TYYP, AUTOMAKS, REGTASU 
            FROM Car 
            WHERE AUTOMAKS IS NOT NULL 
            ORDER BY ESMANE_REG DESC, AUTOMAKS ASC 
            LIMIT 1
        """)
        cheapest_new = curs.fetchone()

        # Query for ⚡ Elektriline (Closest electric car)
        curs.execute("""
            SELECT MARK, MUDEL, ESMANE_REG, MOOTORI_VOIMSUS, KYTUSE_TYYP, AUTOMAKS, REGTASU, ELEKTRILINE_SOIDUULATUS 
            FROM Car 
            WHERE KYTUSE_TYYP = 'ELEKTER' 
            ORDER BY ABS(AUTOMAKS - ?) 
            LIMIT 1
        """, (maks,))
        electric_car = curs.fetchone()

        # Prepare results and filter out None values
        results = [
            ("🌟 Kõige uuem", newest_car),
            ("💪 Kõige võimsam", most_powerful),
            ("💰 Uus ja soodsam", cheapest_new)
        ]

        if electric_car:  # Only add electric if found
            results.append(("⚡ Elektriline", electric_car))

        # Print results in a formatted table
        print("\nLeitud autod (kõige lähemad aastamaksule):")
        print("=" * 130)
        print(f"{'Kategooria':20} {'Mark':15} {'Mudel':20} {'Registreerimine':15} {'Võimsus':10} {'Kütus':10} {'Aastamaks':10} {'RegTasu':10} {'Sõiduulatus':15}")
        print("=" * 130)

        for label, car in results:
            if car:
                if len(car) == 8:  # If it's an electric car, include range
                    mark, mudel, reg, voim, kytus, maks, regtasu, soiduulatus = car
                    print(f"{label:20} {mark:15} {mudel:20} {reg:15} {voim:<10.1f} {kytus:10} {maks:<10.1f} {regtasu:<10.1f} {soiduulatus:15}")
                else:
                    mark, mudel, reg, voim, kytus, maks, regtasu = car
                    print(f"{label:20} {mark:15} {mudel:20} {reg:15} {voim:<10.1f} {kytus:10} {maks:<10.1f} {regtasu:<10.1f} {'-':15}")

    except ValueError:
        print("Palun sisesta kehtiv number!")

    finally:
        conn.close()

if __name__ == '__main__':
    main()
