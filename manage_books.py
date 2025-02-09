import os
from config import *
import json

def vypsat_tridni_knihy():
    vysledky = []
    for cesta_k_souboru in os.listdir(GLOBAL_LOCATION):
        if os.path.isfile(os.path.join(GLOBAL_LOCATION, cesta_k_souboru)):
            vysledky.append(cesta_k_souboru)
    return [i for i in vysledky if (i[-5:] == ".json" and i != "all_students.json") ]

def vytvorit_tridni_knihu(jmeno_tridy, krestni_jmeno_tridniho_ucitele, prijimeni_tridniho_ucitele):
   
    if str(jmeno_tridy) + "json" in vypsat_tridni_knihy():
        return 0
    else:
        f = open(f"{GLOBAL_LOCATION}{jmeno_tridy}.json", "w")
        lokalni_json_tridy = GLOBAL_JSON_STRUCTURE
        lokalni_json_tridy["nazev_tridy"] = jmeno_tridy
        lokalni_json_tridy["jmeno_tridniho_ucitele"] = krestni_jmeno_tridniho_ucitele + " " + prijimeni_tridniho_ucitele
        f.write(json.dumps(lokalni_json_tridy, ensure_ascii=False))
        f.close()
        return 1
    
def smaz_zaznam_tridni_knihy(jmeno_tridy):
    if jmeno_tridy + ".json" in vypsat_tridni_knihy():
        with open(GLOBAL_LOCATION + jmeno_tridy + ".json", "w") as trida_na_smazani:
            trida_na_smazani.write("")
        return 1
    else: return 0

def nacist_tridni_knihu(jmeno_tridy):
    if jmeno_tridy + ".json" in vypsat_tridni_knihy():
        with open(GLOBAL_LOCATION + jmeno_tridy + ".json", "r") as tridni_kniha_json:

            return json.loads(tridni_kniha_json.read())
        
def aktualizovat_tridni_knihu(tridni_kniha_json):
    if tridni_kniha_json["nazev_tridy"] + ".json" in vypsat_tridni_knihy():
        with open(GLOBAL_LOCATION + tridni_kniha_json["nazev_tridy"] + ".json", "w") as tk:
            tk.write(json.dumps(tridni_kniha_json, indent=2, ensure_ascii=False))

def vypis_jmena_vsech_zaku():
    with open(GLOBAL_LOCATION + "all_students.json", "r") as all_students:
        return json.loads(all_students.read())
class karta_zaka:
    def __init__(self, jmeno, prijimeni, datum_narozeni, trida):
        self.karta = GLOBAL_STUDENT_JSON_STRUCTURE
        self.karta["jmeno_zaka"] = jmeno
        self.karta["prijimeni_zaka"] = prijimeni
        self.karta["datum_narozeni"] = datum_narozeni
        self.karta["trida"] = trida
      
    def ulozit_do_tridnicke_knihy(self):        
        if not self.karta["trida"] + ".json" in vypsat_tridni_knihy():
            return 0
        else:
            index_jmena = 1
            vsichni_studenti = vypis_jmena_vsech_zaku()
            jmeno = self.karta["jmeno_zaka"]
            prijimeni = self.karta["prijimeni_zaka"]
            while True:
                if jmeno + prijimeni + str(index_jmena) in vsichni_studenti:
                    index_jmena += 1
                    continue
                else:
                    self.karta["username"] = jmeno + prijimeni + str(index_jmena)
                    vsichni_studenti.append(jmeno + prijimeni + str(index_jmena))
                    with open(GLOBAL_LOCATION + "all_students.json", "w") as a:
                        a.write(json.dumps(vsichni_studenti, ensure_ascii=False))
                    break
            lokalni_tridni_kniha = nacist_tridni_knihu(self.karta["trida"])
            print(vypis_jmena_vsech_zaku()         )       
            lokalni_tridni_kniha["zaci"][self.karta["username"]] = (self.karta)
            aktualizovat_tridni_knihu(lokalni_tridni_kniha)

class bcolors:
    HEADER = '\033[95m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def pridelit_znamku( username, znamka, uloha, trida = None):
    if trida != None:
        tridni_kniha_local = nacist_tridni_knihu(trida)
        # print(json.dumps(tridni_kniha_local, indent=1, ensure_ascii=False))
        if uloha not in list(tridni_kniha_local["znamky"]):
            tridni_kniha_local["znamky"][uloha] = {}
        tridni_kniha_local["znamky"][uloha][username] = znamka
        if username in tridni_kniha_local["zaci"]:
            aktualizovat_tridni_knihu(tridni_kniha_local)
        else: return 0
# import requests
# import random
# word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

# response = requests.get(word_site)
# WORDS = response.content.splitlines()

# for i in range(15):
#     w1 = WORDS[random.randrange(len(WORDS))].decode('ASCII')
#     w2 = WORDS[random.randrange(len(WORDS))].decode('ASCII')
#     zak = karta_zaka(jmeno=w1, prijimeni=w2, datum_narozeni=1, trida="6a")
#     zak.ulozit_do_tridnicke_knihy()
# vytvorit_tridni_knihu("6a", "Luboš Navrátil")
# zak = karta_zaka(jmeno="Lukáš", prijimeni="Karel", datum_narozeni=4, trida="6a")
# zak.ulozit_do_tridnicke_knihy()
# print(pridelit_znamku("LukášKarel5", 4, uloha="úkol", trida="6a"))
def udelej_tabulku_se_znamkami(trida):
    USERNAMES = "USERNAMES"

    header_poznamky = [{"nazev":x, "sirka_sloupce":max(len(x), 3)} for x in [i for i in nacist_tridni_knihu("6a")["znamky"]] ]
    header_poznamky = {x:max(len(x) + 3, 3) for x in   [i for i in nacist_tridni_knihu("6a")["znamky"]]}

    slovnik_znamek_podle_jmen = {}
    for zak_username in nacist_tridni_knihu("6a")["zaci"]:
        slovnik_znamek_podle_jmen[zak_username] = {}
        for x in nacist_tridni_knihu("6a")["znamky"]:
            if zak_username in nacist_tridni_knihu("6a")["znamky"][x]:
                slovnik_znamek_podle_jmen[zak_username][x] = str(nacist_tridni_knihu("6a")["znamky"][x][zak_username])
            else:
                slovnik_znamek_podle_jmen[zak_username][x] = " "

    whole_string_of_table = ""
    username_coll = [USERNAMES] + [i for i in slovnik_znamek_podle_jmen]
    max_col = max([len(i) + 5 for i in username_coll])

    serparator = "+" + "-"*max_col + "++" + "-+-".join([f"{header_poznamky[znamka]*"-":^{header_poznamky[znamka]}}" for znamka in slovnik_znamek_podle_jmen[next(iter(slovnik_znamek_podle_jmen))]])
    whole_string_of_table += serparator + "\n"

    whole_string_of_table += f"{USERNAMES:>{max_col}}" + " ||" +  " | ".join([f"{i :^{header_poznamky[i]}}" for i in header_poznamky]) + "\n"
    header = []
    whole_string_of_table += serparator + "\n"
    index_studenta = 1
    for i in slovnik_znamek_podle_jmen:
        jmeno_s_indexem = f"{i} [{str(100 + index_studenta)[1:]}]"
        znamky_studenta_v_radku =f"{jmeno_s_indexem  :>{max_col}}" + " ||" +  " | ".join([f"{slovnik_znamek_podle_jmen[i][znamka]:^{ header_poznamky[znamka]}}" for znamka in slovnik_znamek_podle_jmen[i]])
        student_jmeno_formatovan = f"{i:>{20}}"
        whole_string_of_table +=  znamky_studenta_v_radku + "\n"
        whole_string_of_table += serparator + "\n"
        index_studenta += 1
    print( whole_string_of_table)


valid_znamky = [i/2 for i in range(2, 11)]
if __name__ == "__main__":
    vytvorit_tridni_knihu(*["2a", "Zbyňek", "Kopýtko"])
    print(nacist_tridni_knihu("2a"))
    import random
    # zak = karta_zaka(jmeno="petr", prijimeni="fialka", trida="1a", datum_narozeni="4sdfgwe")
    # zak.ulozit_do_tridnicke_knihy()

    for i in ["petrfialka1", "petrfialka2", "petrfialka3", "petrfialka4", "petrfialka5", "petrfialka6", "petrfialka7", "petrfialka8", "petrfialka9", "petrfialka10", "petrfialka11"]:
        pridelit_znamku(username=i, znamka=1, uloha=str(random.randrange(104, 109)), trida="1a")