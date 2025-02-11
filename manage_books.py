import os
from config import *
import json

def list_all_class_books():
    filenames_unfiltered = []
    for filepath in os.listdir(GLOBAL_LOCATION):
        if os.path.isfile(os.path.join(GLOBAL_LOCATION, filepath)):
            filenames_unfiltered.append(filepath)
    return [filename for filename in filenames_unfiltered if (filename[-5:] == ".json" and filename != "all_students.json") ]


class class_book:
    def __init__(self, classname, teacher_first_name, teacher_last_name):
        self.class_book = GLOBAL_JSON_STRUCTURE
        self.class_book["class_name"] = classname
        self.class_book["name_of_teacher"] = teacher_first_name + " " + teacher_last_name
    def write_class_book(self):
        if self.class_book["class_name"] + ".json" in list_all_class_books():
            raise ValueError("Třída již existuje")
        with open(GLOBAL_LOCATION + self.class_book["class_name"] + ".json", "w") as f:
            f.write(json.dumps(self.class_book, indent=1, ensure_ascii=False))


    


    
def delete_record_of_class_book(classname):
    if classname + ".json" in list_all_class_books():
        os.remove(GLOBAL_LOCATION + classname + ".json") 
        # with open(GLOBAL_LOCATION + classname + ".json", "w") as record_to_be_deleted:
        #     record_to_be_deleted.write("")
        return 1
    else: return 0

def load_class_book(classname):
    if classname + ".json" in list_all_class_books():
        try:
            with open(GLOBAL_LOCATION + classname + ".json", "r") as class_book_json:

                return json.loads(class_book_json.read())
        except FileNotFoundError:
            raise ValueError("soubor nenalezen")
        
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
        
        if len(date_of_birth.split(".")) == 3:
            self.card["date_of_birth"] = date_of_birth
        else:
            raise ValueError("Datum narození musí být ve formátu dd.mm.yyyy")
        
        if class_name + ".json" in list_all_class_books():
            self.card["class_name"] = class_name
        else:
            raise ValueError("Třída neexistuje")
      
    def save_record_to_classbook(self):        
        if not self.card["class_name"] + ".json" in list_all_class_books():
            return 0
        else:
            replacing_special_character_table = {"á":"a", "č":"c", "ď":"d", "éě":"e", "í":"i", "ň":"n", "ó":"o", "ř":"r", "š":"s", "ť":"t", "úů":"u", "ý":"y", "ž":"z"}

            name_index = 1
            all_students = list_names_of_all_students()
            name = self.card["student_first_name"]
            decapitalised_name = name.lower()
            lastname = self.card["student_last_name"]
            decapitalised_lastname = lastname.lower()
            for i in replacing_special_character_table:
                for j in i:
                    decapitalised_name = decapitalised_name.replace(j, replacing_special_character_table[i])
                    decapitalised_lastname = decapitalised_lastname.replace(j, replacing_special_character_table[i])
            
            decapitalised_lastname = decapitalised_lastname[:5]
            decapitalised_name = decapitalised_name[:2]


            while True:
                
                if decapitalised_lastname + decapitalised_name + str(name_index) in all_students:
                    name_index += 1
                    continue
                else:
                    self.card["username"] = decapitalised_lastname + decapitalised_name + str(name_index)
                    all_students.append(decapitalised_lastname + decapitalised_name + str(name_index))
                    with open(GLOBAL_LOCATION + "all_students.json", "w") as a:
                        a.write(json.dumps(all_students, ensure_ascii=False))
                    break
            local_class_book = load_class_book(self.card["class_name"])
            print(list_names_of_all_students()         )       
            local_class_book["students"][self.card["username"]] = (self.card)
            update_class_book(local_class_book)


def delete_student(username, classname):
    if classname + ".json" in list_all_class_books():
        classbook = load_class_book(classname)
        if username in classbook["students"]:
            del classbook["students"][username]
            update_class_book(classbook)
            for i in classbook["marks"]:
                if username in classbook["marks"][i]:
                    del classbook["marks"][i][username]
            return 1
        else:
            return 0
    else:
        return 0


def create_student(name, lastname, date_of_birth, class_name):
    student_card = student_record(name=name, lastname=lastname, date_of_birth=date_of_birth, class_name=class_name)
    student_card.save_record_to_classbook()
    return 1

def give_mark( username, mark, activity_name, class_name):    

    if class_name + ".json" not in list_all_class_books():
        raise ValueError("Třída neexistuje")

    if float(mark) not in [i/2 for i in range(2, 11)]: 
        
        raise ValueError(f"Známka musí být číslo z množiny {[i/2 for i in range(2, 11)]}")
    

    else:
        classbook = load_class_book(class_name)
        if activity_name not in list(classbook["marks"]):
            classbook["marks"][activity_name] = {}
        classbook["marks"][activity_name][username] = mark
        if username in classbook["students"]:
            update_class_book(classbook)
    
        else: raise ValueError("Student není v třídě")


if __name__ == "__main__":
    # a = class_book("1a", "Petr", "Lubomír")
    # a.write_class_book()
    create_student("Lucie", "Vánksá", "12.2.2000", "Septima B")