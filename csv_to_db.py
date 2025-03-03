import sqlite3

def arvuta_maksud(soiduki_tyyp, soiduk_on_elamu, esmaregistreerimine, taismass, mootori_tyyp, co2_standard, co2_heide):
    """
    Calculates vehicle tax and registration fee. Takes all inputs as strings and converts inside.
    Returns values as strings.
    """

    # Convert strings to proper data types
    current_year = 2025
    age = current_year - int(esmaregistreerimine) if esmaregistreerimine.isdigit() else 0
    taismass = int(taismass) if taismass.isdigit() else 0
    co2_heide = int(co2_heide) if co2_heide.isdigit() else 0

    # Handle Boolean-like string for "elamu"
    soiduk_on_elamu = soiduk_on_elamu.strip().lower() in ["true", "yes", "1"]

    # Age-based multiplier (§ 14)
    def age_multiplier(age):
        age_brackets = {
            5: 0.92, 6: 0.84, 7: 0.75, 8: 0.67, 9: 0.59, 10: 0.51,
            11: 0.43, 12: 0.35, 13: 0.26, 14: 0.18, 15: 0.1, 20: 0.0
        }
        for limit, multiplier in age_brackets.items():
            if age >= limit:
                return multiplier
        return 1.0

    mult = age_multiplier(age)

    # Special handling for electric vehicles
    if mootori_tyyp.lower() == "täiselektriline":
        mass_extra = max(0, taismass - 2400) * 0.40
        mass_extra = min(mass_extra, 440)  # Max cap at 440 €
        automaks = 50 + mass_extra

        reg_mass = max(0, taismass - 2400) * 2
        reg_mass = min(reg_mass, 2200)  # Max cap at 2200 €
        registreermistasu = 150 + reg_mass

        return str(round(automaks, 2)), str(round(registreermistasu, 2))

    # N1 category (Elamu vehicles)
    if soiduk_on_elamu:
        base_tax = 50
        if co2_heide > 204:
            co2_tax = (co2_heide - 204) * 3
            if co2_heide > 250:
                co2_tax += (co2_heide - 250) * 0.5
            if co2_heide > 300:
                co2_tax += (co2_heide - 300) * 0.5
        else:
            co2_tax = 0

        mass_component = min(max(0, taismass - 2000) * 0.40, 400)
        tax_raw = base_tax + co2_tax + mass_component
        automaks = base_tax + mult * (tax_raw - base_tax)

        base_reg = 300
        co2_reg = (co2_heide - 204) * 30 if co2_heide > 204 else 0
        reg_raw = base_reg + co2_reg
        registreermistasu = base_reg + mult * (reg_raw - base_reg)

    else:
        # M1 category standard calculations
        base_tax = 50
        if co2_heide > 117:
            co2_tax = (co2_heide - 117) * 3
            if co2_heide > 150:
                co2_tax += (co2_heide - 150) * 0.5
            if co2_heide > 200:
                co2_tax += (co2_heide - 200) * 0.5
        else:
            co2_tax = 0

        mass_component = min(max(0, taismass - 2000) * 0.40, 400)
        tax_raw = base_tax + co2_tax + mass_component
        automaks = base_tax + mult * (tax_raw - base_tax)

        base_reg = 150
        co2_reg = (co2_heide - 117) * 10 if co2_heide > 117 else 0
        reg_mass = min(max(0, taismass - 2000) * 2, 2000)
        reg_raw = base_reg + co2_reg + reg_mass
        registreermistasu = base_reg + mult * (reg_raw - base_reg)

    return str(round(automaks, 2)), str(round(registreermistasu, 2))

def process_vehicle_data(file_path, filter_criteria=None, output_file=None, delimiter=';', encoding='utf-8'):
    """
    Töötleb sõidukite andmeid CSV-failist, teostab andmeanalüüsi ja võimaldab filtreerimist.
    
    Args:
        file_path (str): CSV-faili asukoht
        filter_criteria (dict, optional): Filtreerimise kriteeriumid (nt {"MARK": "TOYOTA"})
        output_file (str, optional): Väljundfaili asukoht filtreeritud andmete jaoks
        delimiter (str, optional): CSV-faili eraldaja (vaikimisi ';')
        encoding (str, optional): Faili kodeering (vaikimisi 'utf-8')
        
    Returns:
        tuple: (sõidukite andmed, analüüsi tulemused)
    """
    import csv
    import os
    
    def parse_csv(file_path, delimiter=';', encoding='utf-8'):
        """
        Loeb sisse CSV-faili ja tagastab sõidukite andmed.
        """
        vehicles = []
        
        try:
            with open(file_path, 'r', encoding=encoding) as csvfile:
                i = 0

                reader = csv.DictReader(csvfile, delimiter=delimiter)
                for row in reader:
                    automaks, registreermistasu = arvuta_maksud(
                        soiduki_tyyp=row["KATEGOORIA"],
                        soiduk_on_elamu=(row["KERE_NIMETUS"]),
                        esmaregistreerimine=row["ESMANE_REG"][:4],  # Võtame ainult aasta osa
                        taismass=row["TAISMASS"],
                        mootori_tyyp=row["MOOTORI_TYYP"],
                        co2_standard="WLTP",  # Eeldame, et kasutame WLTP
                        co2_heide=row["CO2_WLTP"]
                    )
                    row["MARK"] = row["\ufeffMARK"]
                    row['AUTOMAKS'] = float(automaks)
                    row['REGTASU'] = float(registreermistasu)
                    row["ID"] = i
                    i = i + 1
                    vehicles.append(row)

                print(f"Edukalt loetud {len(vehicles)} sõiduki andmed.")
            return vehicles
        
        except Exception as e:
            print(f"Viga faili lugemisel: {e}")
            return []
    
    # Loe andmed CSV-failist
    vehicles = parse_csv(file_path, delimiter, encoding)

    return vehicles

def init_db():
    curs.execute('''
CREATE TABLE IF NOT EXISTS Car (
    ALAMKATEGOORIA TEXT,
    AUTORONGI_MASS INTEGER,
    CO2_NEDC INTEGER,
    CO2_WLTP INTEGER,
    EESTIS_ESMAREG TEXT,
    ELEKTRILINE_SOIDUULATUS TEXT,
    ESMANE_REG TEXT,
    HAAGIS_PIDURITEGA INTEGER,
    HAAGIS_PIDURITETA INTEGER,
    HAAKESEADME_KOORMUS INTEGER,
    HEITMENORM TEXT,
    HYBRIIDI_TYYP TEXT,
    ISTEKOHTI INTEGER,
    JUHTTELGI INTEGER,
    KAIGUKASTI_TYYP TEXT,
    KATEGOORIA TEXT,
    KERETYYP TEXT,
    KERE_NIMETUS TEXT,
    KORGUS INTEGER,
    KYTUSEKOMBINATSIOON TEXT,
    KYTUSEKULU_KESK_NEDC REAL,
    KYTUSEKULU_KESK_WLTP REAL,
    KYTUSE_TYYP TEXT,
    LAIUS INTEGER,
    LISAKYTUS TEXT,
    MOOTORI_MAHT INTEGER,
    MOOTORI_TYYP TEXT,
    MOOTORI_VOIMSUS REAL,
    MUDEL TEXT,
    PIKKUS INTEGER,
    RATTAID INTEGER,
    REG_MASS INTEGER,
    SOIDUMYRA REAL,
    STAATUS TEXT,
    SUURIM_KIIRUS INTEGER,
    TAISMASS INTEGER,
    TELGI_KOKKU INTEGER,
    TYHIMASS INTEGER,
    TYYP TEXT,
    UKSI INTEGER,
    VARV TEXT,
    VEOTELGI INTEGER,
    VKOM_MAAKOND TEXT,
    VKOM_TYYP TEXT,
    YLDINE_STAATUS TEXT,
    MARK TEXT,
    AUTOMAKS REAL,
    REGTASU REAL,
    ID INT
)
''')

conn = sqlite3.connect('cars.db')
curs = conn.cursor()

init_db()

vehicles = process_vehicle_data('autod.csv')

insert_query = '''
INSERT INTO Car (
    ALAMKATEGOORIA, AUTORONGI_MASS, CO2_NEDC, CO2_WLTP, EESTIS_ESMAREG, 
    ELEKTRILINE_SOIDUULATUS, ESMANE_REG, HAAGIS_PIDURITEGA, HAAGIS_PIDURITETA, 
    HAAKESEADME_KOORMUS, HEITMENORM, HYBRIIDI_TYYP, ISTEKOHTI, JUHTTELGI, 
    KAIGUKASTI_TYYP, KATEGOORIA, KERETYYP, KERE_NIMETUS, KORGUS, 
    KYTUSEKOMBINATSIOON, KYTUSEKULU_KESK_NEDC, KYTUSEKULU_KESK_WLTP, 
    KYTUSE_TYYP, LAIUS, LISAKYTUS, MOOTORI_MAHT, MOOTORI_TYYP, 
    MOOTORI_VOIMSUS, MUDEL, PIKKUS, RATTAID, REG_MASS, SOIDUMYRA, STAATUS, 
    SUURIM_KIIRUS, TAISMASS, TELGI_KOKKU, TYHIMASS, TYYP, UKSI, VARV, VEOTELGI, 
    VKOM_MAAKOND, VKOM_TYYP, YLDINE_STAATUS, MARK, AUTOMAKS, REGTASU, ID
) VALUES (
    :ALAMKATEGOORIA, :AUTORONGI_MASS, :CO2_NEDC, :CO2_WLTP, :EESTIS_ESMAREG, 
    :ELEKTRILINE_SOIDUULATUS, :ESMANE_REG, :HAAGIS_PIDURITEGA, :HAAGIS_PIDURITETA, 
    :HAAKESEADME_KOORMUS, :HEITMENORM, :HYBRIIDI_TYYP, :ISTEKOHTI, :JUHTTELGI, 
    :KAIGUKASTI_TYYP, :KATEGOORIA, :KERETYYP, :KERE_NIMETUS, :KORGUS, 
    :KYTUSEKOMBINATSIOON, :KYTUSEKULU_KESK_NEDC, :KYTUSEKULU_KESK_WLTP, 
    :KYTUSE_TYYP, :LAIUS, :LISAKYTUS, :MOOTORI_MAHT, :MOOTORI_TYYP, 
    :MOOTORI_VOIMSUS, :MUDEL, :PIKKUS, :RATTAID, :REG_MASS, :SOIDUMYRA, :STAATUS, 
    :SUURIM_KIIRUS, :TAISMASS, :TELGI_KOKKU, :TYHIMASS, :TYYP, :UKSI, :VARV, :VEOTELGI, 
    :VKOM_MAAKOND, :VKOM_TYYP, :YLDINE_STAATUS, :MARK, :AUTOMAKS, :REGTASU, :ID
)
'''

for v in vehicles:
    curs.execute(insert_query, v)

conn.commit()
conn.close()
