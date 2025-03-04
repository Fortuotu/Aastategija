import random
import time

class Auto:
    def __init__(self, mark, mudel, vaartus, mootori_maht, co2_heitkogused, vanus):
        self.mark = mark
        self.mudel = mudel
        self.vaartus = vaartus
        self.mootori_maht = mootori_maht  # liitrites
        self.co2_heitkogused = co2_heitkogused  # g/km
        self.vanus = vanus  # aastates
        
    def __str__(self):
        return f"{self.mark} {self.mudel} ({self.vaartus:,}€, {self.mootori_maht}L, {self.co2_heitkogused}g/km CO2, {self.vanus} aastat vana)"

def arvuta_maks(auto):
    """Arvutab automaksu sõiduki omaduste põhjal - lihtsustatud versioon"""
    # Lihtne maksuarvestus CO2 heitkoguste põhjal - ümardatud lähima 50-ni
    heitkoguse_maks = (auto.co2_heitkogused // 50) * 50
    
    # Elektriautod on maksuvabad
    if auto.mootori_maht == 0:
        heitkoguse_maks = 0
    
    # Vanusega seotud kohandused - vanematel autodel on teistsugune maksusüsteem
    if auto.vanus > 15:  # Alandatud 20-lt 15-le, et rohkem autosid oleks maksuvabad
        # Ajaloolised sõidukid on maksuvabad
        return 0
    
    # Luksusautode maks - lihtsustatud
    luksus_maks = 0
    if auto.vaartus > 40000 and auto.vanus <= 5:
        luksus_maks = 300  # Alandatud 350-lt
        
    return heitkoguse_maks + luksus_maks

def genereeri_juhuslik_auto():
    """Genereerib juhusliku auto lihtsate väärtustega"""
    margid = ["Toyota", "Ford", "BMW", "Tesla", "Honda", "Volkswagen"]
    mudelid = ["Sedaan", "Maastur", "Elektriline", "Luukpära"]
    
    mark = random.choice(margid)
    mudel = random.choice(mudelid)
    
    # Tesla ja Elektrilised mudelid on alati elektrilised
    on_elektriline = (mark == "Tesla" or mudel == "Elektriline" or random.random() < 0.2)
    
    if on_elektriline:
        mootori_maht = 0
        co2_heitkogused = 0
    else:
        # Lihtsustatud - mootori mahud on nüüd täisarvud
        mootori_maht = random.randint(1, 3)
        # CO2 heitkogused on nüüd korrutised 50-ga lihtsama arvutamise jaoks
        co2_heitkogused = random.choice([50, 100, 150, 200, 250])
    
    # Lihtsustatud väärtuste vahemikud
    vaartus = random.choice([10000, 20000, 30000, 45000, 60000])
    # Lihtsamad vanusevahemikud
    vanus = random.choice([0, 3, 8, 12, 18])
    
    return Auto(mark, mudel, vaartus, mootori_maht, co2_heitkogused, vanus)

def puhasta_ekraan():
    """Puhastab ekraani parema loetavuse jaoks"""
    print("\n" * 10)

def kirjutamise_efekt(tekst):
    """Loob teksti jaoks kirjutamise efekti (kiirem)"""
    for taht in tekst:
        print(taht, end='', flush=True)
        time.sleep(0.01)  # Kiirem kirjutamine
    print()

def mangi_mangu():
    mangija_nimi = input("Tere tulemast Automaksu Seiklusesse! Mis on sinu nimi? ")
    puhasta_ekraan()
    
    kirjutamise_efekt(f"Tere tulemast, {mangija_nimi}! Oled maksuspetsialist Maanteeametis.")
    kirjutamise_efekt("Sinu ülesanne on arvutada erinevate sõidukite õige maks.")
    kirjutamise_efekt("Ära muretse - aitame sind selle teekonna jooksul!")
    
    punktid = 0
    tase = 1
    elud = 5  # Suurendatud 3-lt
    hinnatud_autod = 0
    
    while elud > 0:
        puhasta_ekraan()
        print(f"===== TASE {tase} =====")
        print(f"Punktid: {punktid}  |  Elud: {'❤' * elud}  |  Hinnatud autod: {hinnatud_autod}")
        print(f"Maksuspetsialisti auaste: {saa_auaste(punktid)}")
        print("=" * 20)
        
        # Genereerib autosid vastavalt praegusele tasemele
        auto = genereeri_juhuslik_auto()
        
        print(f"\nSinu juurde saabus {auto} maksuhindamiseks.")
        
        # Näitab alati maksuarvutuse juhendeid
        print("\nMAKSUARVUTUSE JUHEND:")
        print("1. Põhimaks võrdub CO2 heitkogusega (g/km)")
        print("   - Elektrisõidukid (0L mootor) maksavad 0€")
        print("2. Autod üle 40 000€ lisavad 300€ luksusmaksu esimeseks 5 aastaks")
        print("3. Autod üle 15 aasta vanused on maksuvabad (0€)")
        
        # Näitab täpset arvutust selle auto jaoks vihjeks
        if auto.vanus > 15:
            print("\nVIHJE: See auto on üle 15 aasta vana, seega on maksuvaba (0€)")
        elif auto.mootori_maht == 0:
            if auto.vaartus > 40000 and auto.vanus <= 5:
                print("\nVIHJE: See on elektriauto (luksusklass), seega maks = 300€")
            else:
                print("\nVIHJE: See on elektriauto, seega maks = 0€")
        else:
            alus = auto.co2_heitkogused
            luksus = 300 if auto.vaartus > 40000 and auto.vanus <= 5 else 0
            print(f"\nVIHJE: Maks = {alus} (CO2) + {luksus} (luksus) = {alus + luksus}€")
        
        oige_maks = arvuta_maks(auto)
        
        # Laseb mängijal mõelda
        time.sleep(1)
        
        # Võimalus arvutus vahele jätta
        jata_valik = input("\nKas soovid arvutuse vahele jätta ja vastust näha? (j/e): ").lower()
        if jata_valik.startswith('j'):
            kirjutamise_efekt(f"Õige maks on {oige_maks}€.")
            punktid += 50  # Väike punktisumma vahelejätmise eest
            hinnatud_autod += 1
            input("\nVajuta Enterit jätkamiseks...")
            continue
        
        try:
            mangija_vastus = int(input("\nKui palju maksu tuleks maksta? "))
            
            # Lubab palju suuremat veavaru (25% või 50€, kumb on suurem)
            varu = max(50, oige_maks * 0.25)
            if abs(mangija_vastus - oige_maks) <= varu:
                kirjutamise_efekt("\n✓ Õige! Tubli töö!")
                punktid += tase * 100
                hinnatud_autod += 1
                
                # Aeglasem raskusastme tõus
                if hinnatud_autod % 8 == 0:  # Muudetud 5-lt 8-le
                    tase += 1
                    kirjutamise_efekt(f"\nPalju õnne! Sind edutati tasemele {tase}!")
                    kirjutamise_efekt(f"Sinu uus auaste: {saa_auaste(punktid)}")
                    
                    # Sagedasemad lisaelud
                    if tase % 2 == 0:  # Muudetud 3-lt 2-le
                        elud += 1
                        kirjutamise_efekt("Said ühe lisaelu! ❤")
            else:
                kirjutamise_efekt(f"\n✗ Lähedal, aga mitte päris. Õige maks on {oige_maks}€.")
                selgita_maksu(auto, oige_maks)
                # Valede vastuste eest kaotab ainult pool elu
                if random.random() < 0.5:
                    elud -= 1
                    kirjutamise_efekt("Kaotasid ühe elu.")
                else:
                    kirjutamise_efekt("Su ülemus on täna heas tujus - elu ei läinud!")
                
                if elud > 0:
                    kirjutamise_efekt(f"Sul on {elud} {'elu' if elud == 1 else 'elu'} alles.")
                    
        except ValueError:
            kirjutamise_efekt("\n✗ Palun sisesta kehtiv number.")
            kirjutamise_efekt("Su ülemus on andestavameelne - elu ei läinud.")
        
        input("\nVajuta Enterit jätkamiseks...")
    
    # Mäng läbi
    puhasta_ekraan()
    kirjutamise_efekt("MÄNG LÄBI!")
    kirjutamise_efekt(f"Lõpptulemus: {punktid}")
    kirjutamise_efekt(f"Õigesti hinnatud autod: {hinnatud_autod}")
    kirjutamise_efekt(f"Lõplik auaste: {saa_auaste(punktid)}")
    
    mangi_uuesti = input("\nKas soovid uuesti mängida? (jah/ei): ").lower()
    if mangi_uuesti.startswith("j"):
        mangi_mangu()
    else:
        kirjutamise_efekt("Täname Automaksu Seikluse mängimise eest! Head aega!")

def saa_auaste(punktid):
    """Tagastab auastme mängija punktide põhjal - lihtsam edasiliikumine"""
    if punktid < 300:
        return "Nooreminspektor"
    elif punktid < 800:
        return "Maksuinspektor"
    elif punktid < 1500:
        return "Vaneminspektor"
    elif punktid < 2500:
        return "Peainspektor"
    elif punktid < 4000:
        return "Piirkonna Maksujuht"
    else:
        return "Riiklik Maksuvolinik"

def selgita_maksu(auto, maksu_summa):
    """Selgitab, kuidas maks arvutati - rohkemate üksikasjadega"""
    print("\nÜksikasjalik maksu selgitus:")
    
    if auto.vanus > 15:
        print("See sõiduk on üle 15 aasta vana ja klassifitseeritud ajalooliseks.")
        print("Ajaloolised sõidukid on automaksust täielikult vabastatud.")
        print("Tasumisele kuuluv maks: 0€")
        return
    
    if auto.mootori_maht == 0:
        print("See on elektriauto nullheitega.")
        print("Standardne heitkoguse maks: 0€")
    else:
        print(f"Põhimaks CO2 heitkoguste eest: {auto.co2_heitkogused}€")
    
    if auto.vaartus > 40000 and auto.vanus <= 5:
        print("See on klassifitseeritud kui premium-sõiduk (väärtus üle 40 000€)")
        print("Täiendav luksusmaks: 300€")
        print(f"Kokku tasumisele kuuluv maks: {maksu_summa}€")
    else:
        print(f"Kokku tasumisele kuuluv maks: {maksu_summa}€")

if __name__ == "__main__":
    mangi_mangu()