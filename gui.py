import manage_books
import os 
import json
import datetime
import config 
class Gui:
    def __init__(self):
        self.t_size = (os.get_terminal_size().lines - 2, os.get_terminal_size().columns)
        self.fce = {"cela_tk": self.html_templater, "napoveda":self.napoveda, "konec":self.konec, "nova_tk":self.nova_tk, "vsechny":self.vypis_vsechny_tridni_knihy, "znamky":self.znamky_tridy, "pridel_znamku":self.pridel_znamku}
        odsazeni = "\n"*(self.t_size[0]//2)
        welcome_str = "Vítejte v programu pro správu třídních knih"
        heading_str = "Autor: Štěpán Kovačič"
        print(odsazeni)
        self.print_centered_text(self.c(welcome_str, "purple"), self.c(heading_str, "green"))
        print("\n"*(self.t_size[0]-2 - (2 +(self.t_size[0]//2) )))
        self.refresh_page()

    def html_templater(self, trida):
        print("\n")
        x = manage_books.nacist_tridni_knihu(*trida)
        structure = [ i for i in  manage_books.nacist_tridni_knihu(*trida)]
        # print([manage_books.nacist_tridni_knihu(*trida)[i] for i in structure])
        

        """GLOBAL_JSON_STRUCTURE = {"nazev_tridy":None, 
                         "jmeno_tridniho_ucitele":None, 
                         "zaci":{}, 
                         "znamky":{}}"""
        tablestr = ""
        for i in x["zaci"]:
            l = x["zaci"][i]
            fff =  "<tr><td>" + "</td><td>".join(l.values()) + "</td></tr>"
            tablestr += fff


        seznam_zaku_tridy = [i for i in x["zaci"]]
      

        def catch(func, handle=lambda e : e, *args, **kwargs):
            try:
                return str(func(*args, **kwargs))
            except Exception as e:
                return "-"

        znamky_table_str =  "<tr><th>" + "</th><th>".join(["jmeno"] + [i for i in x["znamky"]]) + "</th></tr>"

        
        for ssdf in seznam_zaku_tridy:
            fff =  "<tr><td>" + "</td><td>".join([ssdf] +  [catch(lambda:x["znamky"][i][ssdf]) for i in x["znamky"]]) + "</td></tr>"
            znamky_table_str += fff

        a = f"""
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
}}</style>
        </head>


        <body>
            <center>
            <h1>Výpis z třídní knihy - {datetime.datetime.now().strftime("%d.%m. %Y %H:%M:%S")}</h1>
            </center>
            <hr>
            <h2>Jméno Třídy: {x["nazev_tridy"]}</h2>
            <h2>Jméno třídního učitele: {x["jmeno_tridniho_ucitele"]}</h2>
           

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
            {tablestr}
            
            </table>
            <hr>
            <h3>Výpis známek</h3>
           
            <table>
            {znamky_table_str}
            
            </table>
            <script>
            window.print();
            </script>
        </body>

        </html>
        """
       
        with open(config.GLOBAL_LOCATION + "html_template.html", "w") as f:
            f.write(a)
        
        command = os.popen(f'open {config.GLOBAL_LOCATION}html_template.html')
        command.read()
        command.close()
        self.refresh_page()

    def print_centered_text(self, *text):
        for t in text:
            print(f"{t:^{self.t_size[1]}}")

    def vypis_vsechny_tridni_knihy(self):
        print("\n")
        vsechny = [i for i in manage_books.vypsat_tridni_knihy() if i != "all_students.json"]
        for i in vsechny:
            print("\t> " , i[:-5])
        self.refresh_page()
           
    def c(self, text, color):
        #funkce se naschvál jmenuje jen c ať v kodu nezabírá moc místa 
        colors = {"purple":'\033[94m', "green":'\033[92m', "red":'\033[91m', "underline":'\033[4m'}
        return colors[color] + text + '\033[0m'
    
    def refresh_page(self, number_of_rows_to_omit=0):
        print("\n")
        # print("\n"*(self.t_size[0]-1 - number_of_rows_to_omit))
        Napoveda_str = "Pro nápovědu napište \"napoveda\" | Pro odchod napište \"konec\""
        print('\x1b[6;30;42m' + Napoveda_str  + (self.t_size[1]  - len(Napoveda_str)) * " " + '\033[0m')
        input_str = input("Zadejte příkaz: ")
        list_of_args = [i for i in input_str.split(" ") if i != ""]
        func_name = list_of_args[0]
        args = list_of_args[1:]
        if args != []:
            self.fce[func_name](args)
        else: self.fce[func_name]()
        
    def znamky_tridy(self, trida):
        print("\n")
        # print(manage_books.nacist_tridni_knihu(*trida))
        print( json.dumps(manage_books.nacist_tridni_knihu(*trida)["znamky"], ensure_ascii=False, indent=2))
        self.refresh_page()
        
    def pridel_znamku(self, text):
        manage_books.pridelit_znamku(*text)
        print("\n")
        print("Byla přidělena známka")
        print("\n")
    def konec(self):
        print("\n"*(self.t_size[0]-1))
        print(self.c("Program ukončen", "green"))
        
    def napoveda(self):
        napoveda_string = """
        Nápověda pro program na správu třídnických knih
        \033[95mSeznam Příkazů\033[0m
          
        \t> [nova_tk <jméno třídy> <křestní jm. t.u.> <prijimeni t.u.>] je příkaz pro vytvoření nové třídní knihy 
          
        \t> [zobraz_tk <jméno třídy>]
          
        \t> [konec] ukončí celý program

        \t> [znamky <jméno třídy>]
          """
        print(napoveda_string)
        self.refresh_page(len(napoveda_string.split("\n")))
    
    def nova_tk(self, args):
        manage_books.vytvorit_tridni_knihu(*args)
        self.vypis_vsechny_tridni_knihy()

x = Gui()