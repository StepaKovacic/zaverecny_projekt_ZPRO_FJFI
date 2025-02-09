import os
from config import *
import json

def list_all_class_books():
    filenames_unfiltered = []
    for filepath in os.listdir(GLOBAL_LOCATION):
        if os.path.isfile(os.path.join(GLOBAL_LOCATION, filepath)):
            filenames_unfiltered.append(filepath)
    return [filename for filename in filenames_unfiltered if (filename[-5:] == ".json" and filename != "all_students.json") ]

def create_class_book(classname, teacher_first_name, teacher_last_name):
   
    if str(classname) + "json" in list_all_class_books():
        return 0
    else:
        f = open(f"{GLOBAL_LOCATION}{classname}.json", "w")
        internal_json_of_class = GLOBAL_JSON_STRUCTURE
        internal_json_of_class["class_name"] = classname
        internal_json_of_class["name_of_teacher"] = teacher_first_name + " " + teacher_last_name
        f.write(json.dumps(internal_json_of_class, ensure_ascii=False))
        f.close()
        return 1
    
def delete_record_of_class_book(classname):
    if classname + ".json" in list_all_class_books():
        with open(GLOBAL_LOCATION + classname + ".json", "w") as record_to_be_deleted:
            record_to_be_deleted.write("")
        return 1
    else: return 0

def load_class_book(classname):
    if classname + ".json" in list_all_class_books():
        with open(GLOBAL_LOCATION + classname + ".json", "r") as class_book_json:

            return json.loads(class_book_json.read())
        
def update_class_book(class_book_json):
    if class_book_json["class_name"] + ".json" in list_all_class_books():
        with open(GLOBAL_LOCATION + class_book_json["class_name"] + ".json", "w") as tk:
            tk.write(json.dumps(class_book_json, indent=2, ensure_ascii=False))

def list_names_of_all_students():
    with open(GLOBAL_LOCATION + "all_students.json", "r") as all_students:
        return json.loads(all_students.read())



class student_record:
    def __init__(self, name, lastname, date_of_birth, class_name):
        self.card = GLOBAL_STUDENT_JSON_STRUCTURE
        self.card["student_first_name"] = name
        self.card["student_last_name"] = lastname
        self.card["date_of_birth"] = date_of_birth
        self.card["class_name"] = class_name
      
    def save_record_to_classbook(self):        
        if not self.card["class_name"] + ".json" in list_all_class_books():
            return 0
        else:
            name_index = 1
            all_students = list_names_of_all_students()
            name = self.card["student_first_name"]
            lastname = self.card["student_last_name"]
            while True:
                if name + lastname + str(name_index) in all_students:
                    name_index += 1
                    continue
                else:
                    self.card["username"] = name + lastname + str(name_index)
                    all_students.append(name + lastname + str(name_index))
                    with open(GLOBAL_LOCATION + "all_students.json", "w") as a:
                        a.write(json.dumps(all_students, ensure_ascii=False))
                    break
            local_class_book = load_class_book(self.card["class_name"])
            print(list_names_of_all_students()         )       
            local_class_book["students"][self.card["username"]] = (self.card)
            update_class_book(local_class_book)





def create_student(name, lastname, date_of_birth, class_name):
    student_card = student_record(name=name, lastname=lastname, date_of_birth=date_of_birth, class_name=class_name)
    student_card.save_record_to_classbook()
    return 1

def give_mark( username, mark, activity_name, class_name = None):
    if mark not in [i/2 for i in range(2, 11)]: 
        print(f"Známka musí být číslo z množiny {set([i/2 for i in range(2, 11)])}")
        return 0
    if class_name != None:
        load_class_book = load_class_book(class_name)
        # print(json.dumps(tridni_kniha_local, indent=1, ensure_ascii=False))
        if activity_name not in list(load_class_book["marks"]):
            load_class_book["marks"][activity_name] = {}
        load_class_book["marks"][activity_name][username] = mark
        if username in load_class_book["students"]:
            update_class_book(load_class_book)
        else: return 0


# def udelej_tabulku_se_znamkami(trida):
#     USERNAMES = "USERNAMES"

#     header_pomarks = [{"nazev":x, "sirka_sloupce":max(len(x), 3)} for x in [i for i in load_class_book("6a")["marks"]] ]
#     header_pomarks = {x:max(len(x) + 3, 3) for x in   [i for i in load_class_book("6a")["marks"]]}

#     slovnik_znamek_podle_jmen = {}
#     for zak_username in load_class_book("6a")["students"]:
#         slovnik_znamek_podle_jmen[zak_username] = {}
#         for x in load_class_book("6a")["marks"]:
#             if zak_username in load_class_book("6a")["marks"][x]:
#                 slovnik_znamek_podle_jmen[zak_username][x] = str(load_class_book("6a")["marks"][x][zak_username])
#             else:
#                 slovnik_znamek_podle_jmen[zak_username][x] = " "

#     whole_string_of_table = ""
#     username_coll = [USERNAMES] + [i for i in slovnik_znamek_podle_jmen]
#     max_col = max([len(i) + 5 for i in username_coll])

#     serparator = "+" + "-"*max_col + "++" + "-+-".join([f"{header_pomarks[znamka]*"-":^{header_pomarks[znamka]}}" for znamka in slovnik_znamek_podle_jmen[next(iter(slovnik_znamek_podle_jmen))]])
#     whole_string_of_table += serparator + "\n"

#     whole_string_of_table += f"{USERNAMES:>{max_col}}" + " ||" +  " | ".join([f"{i :^{header_pomarks[i]}}" for i in header_pomarks]) + "\n"
#     header = []
#     whole_string_of_table += serparator + "\n"
#     index_studenta = 1
#     for i in slovnik_znamek_podle_jmen:
#         jmeno_s_indexem = f"{i} [{str(100 + index_studenta)[1:]}]"
#         marks_studenta_v_radku =f"{jmeno_s_indexem  :>{max_col}}" + " ||" +  " | ".join([f"{slovnik_znamek_podle_jmen[i][znamka]:^{ header_pomarks[znamka]}}" for znamka in slovnik_znamek_podle_jmen[i]])
#         student_jmeno_formatovan = f"{i:>{20}}"
#         whole_string_of_table +=  marks_studenta_v_radku + "\n"
#         whole_string_of_table += serparator + "\n"
#         index_studenta += 1
#     print( whole_string_of_table)


if __name__ == "__main__":
    pass