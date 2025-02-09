import manage_books
import os 
import json
import datetime
import config 
class Gui:
    def __init__(self): 
        self.t_size = (os.get_terminal_size().lines - 2, os.get_terminal_size().columns)

        self.internal_functions_list = {"cela_tk": self.browser_viewer, 
                                        "napoveda":self.hint,
                                        "konec":self.end, 
                                        "nova_tk":self.new_book, 
                                        "vsechny":self.list_all_class_books, 
                                        "znamky":self.marks_by_class, 
                                        "pridel_znamku":self.give_mark, 
                                        "student_info":self.student_info, 
                                        "create_student":self.create_student}
        
        indentation = "\n"*(self.t_size[0]//2)
        welcome_str = "Vítejte v programu pro správu třídních knih"
        heading_str = "Autor: Štěpán Kovačič"
        print(indentation)
        self.print_centered_text(self.colored_text(welcome_str, "purple"), self.colored_text(heading_str, "green"))
        print("\n"*(self.t_size[0]-2 - (2 +(self.t_size[0]//2) )))
        self.refresh_page()

    def browser_viewer(self, class_name): 
        print("\n") 

        print(f"Vytvářím náhled třídní knihy {self.colored_text(class_name[0], 'purple')}")
        print(*class_name)
        loaded_class_book = manage_books.load_class_book(*class_name) 
        unparsed_table_string= ""
        for student in loaded_class_book["students"]:
            student_info = loaded_class_book["students"][student]
            html_ready_row =  "<tr><td>" + "</td><td>".join(student_info.values()) + "</td></tr>"
            unparsed_table_string += html_ready_row

        list_of_class_students = [i for i in loaded_class_book["students"]]
      
        def catch(func,  *args, **kwargs):
            try:
                return str(func(*args, **kwargs))
            except Exception as e:
                return "-"
        marks_to_html_str =  "<tr><th>" + "</th><th>".join(["Username žáka"] + [i for i in loaded_class_book["marks"]]) + "</th></tr>"

        
        for username_student in list_of_class_students:
            username_marks_html_str_row =  "<tr><td>" + "</td><td>".join([username_student] +  [catch(lambda:loaded_class_book["marks"][i][username_student]) for i in loaded_class_book["marks"]]) + "</td></tr>"
            marks_to_html_str += username_marks_html_str_row

        fully_templated_html = f"""
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <title>Třídní kniha - náhled</title>
            <style>
                table {{
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
                }}

                td, th {{
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
                }}

                tr:nth-child(even) {{
                background-color: #dddddd;
                }}
            </style>
        </head>


        <body>
            <center>
                <h1>Výpis z třídní knihy - {datetime.datetime.now().strftime("%d.%m. %Y %H:%M:%S")}</h1>
            </center>
            <hr>
            <h2>Jméno Třídy: {loaded_class_book["class_name"]}</h2>
            <h2>Jméno třídního učitele: {loaded_class_book["name_of_teacher"]}</h2>
           

            <hr>
            <h3>Seznam žáků</h3>
           
            <table>
            <tr>
                <th>Jméno</th>
                <th>Přijímení</th>
                <th>Username</th>
                <th>Datum narození</th>
                <th>Trida</th>
            </tr>
            {unparsed_table_string}
            
            </table>
            <hr>
            <h3>Výpis známek</h3>
           
            <table>
            {marks_to_html_str}
            
            </table>
            <script>
                window.print(); 
            </script>
        </body>

        </html>
        """
       
        with open(config.GLOBAL_LOCATION + "classbook.html", "w") as classbook:
            classbook.write(fully_templated_html) 
        
        command = os.popen(f'open {config.GLOBAL_LOCATION}classbook.html')
        command.read()
        command.close()
        self.refresh_page()

    def create_student(self, args):
        manage_books.create_student(*args)
        self.refresh_page()


    def print_centered_text(self, *text):
        for t in text:
            print(f"{t:^{self.t_size[1]}}")

    def student_info(self, username):
        username = username[0] 

        print(f"\n\tInfo o studentovi {self.colored_text(username, "purple")}")
        all_books = manage_books.list_all_class_books()
        for iter_book in all_books: 
            with open(config.GLOBAL_LOCATION + iter_book, "r") as class_book_json:
                    internal_var_class_book = json.loads(class_book_json.read())
                    if username in (internal_var_class_book["students"]).keys():
                        
                        print("\n", json.dumps(internal_var_class_book["students"][username], indent=2, ensure_ascii=False), "\n")
                        marks_by_username = ([activity_name for activity_name in internal_var_class_book["marks"] if username in internal_var_class_book["marks"][activity_name]])
                        marks_of_user = {}
                        for mark_desctiption in marks_by_username:
                            marks_of_user[mark_desctiption] = float(internal_var_class_book["marks"][mark_desctiption][username])
                        print("{:<20}|{:>8}".format('Úloha','Známka'))
                        print("-" * 29)
                        for k, v in marks_of_user.items():
                            print("{:<20}|{:>8}".format(k, v))
                        print(f"\nAritmetický průměr známek žáka {self.colored_text(username, "purple")} je {self.colored_text(str(round(sum(marks_of_user.values())/len(marks_of_user), 2)), "purple")}")
        self.refresh_page()

    def list_all_class_books(self):
        print("\n")

        print("\tZde jsou vypsány všechny třídní knihy")
        all_books = [i for i in manage_books.list_all_class_books() if i != "all_students.json"]
        for iter_bookname in all_books:
            print("\t> " , iter_bookname[:-5])
        self.refresh_page()
           
    def colored_text(self, text, color):
        colors = {"purple":'\033[94m', "green":'\033[92m', "red":'\033[91m', "underline":'\033[4m'}
        return colors[color] + text + '\033[0m'
    
    def refresh_page(self):
        print("\n")
        help_string = "Pro nápovědu napište \"napoveda\" | Pro odchod napište \"konec\""
        print('\x1b[6;30;42m' + help_string  + (self.t_size[1]  - len(help_string)) * " " + '\033[0m')
        input_str = input("Zadejte příkaz: ")
        # handle if the input is empty
        if input_str == "":
            print("\n")
            print(self.colored_text("Nebyl zadán žádný příkaz", "red"))
            self.refresh_page()
        list_of_args = [i for i in input_str.split(" ") if i != ""]
        func_name = list_of_args[0]
        args = list_of_args[1:]
        print(args)
        try: 
            if args != []:
                self.internal_functions_list[func_name](args)
            else: self.internal_functions_list[func_name]()
        except KeyError:
            print("\n")

            print(self.colored_text(f"Neznámý příkaz \"{input_str}\"", "red"))
            
            self.refresh_page()
        
        
    def marks_by_class(self, class_name):
        print("\n")
        # print(manage_books.load_class_book(*trida))
        print( json.dumps(manage_books.load_class_book(*class_name)["marks"], ensure_ascii=False, indent=2))
        self.refresh_page()
        
    def give_mark(self, text):
        manage_books.give_mark(*text)
        print("\n")
        print("Byla přidělena známka")
        print("\n")
    def end(self):
        print("\n"*(self.t_size[0]-1))
        print(self.colored_text("Program ukončen", "green"))
        
    def hint(self):
        help_string = """
        Nápověda pro program na správu třídnických knih
        \033[95mSeznam Příkazů\033[0m
          
        \t> [nova_tk <jméno třídy> <křestní jm. t.u.> <prijimeni t.u.>] je příkaz pro vytvoření nové třídní knihy 
          
        \t> [zobraz_tk <jméno třídy>] 
          
        \t> [konec] ukončí celý program

        \t> [znamky <jméno třídy>]
          """
        print(help_string)
        self.refresh_page()
    
    def new_book(self, args):
        manage_books.create_class_book(*args)
        self.vypis_vsechny_tridni_knihy()

x = Gui()