import manage_books
import os 
class gui:
    def __init__(self):
        self.t_size = (os.get_terminal_size().lines - 2, os.get_terminal_size().columns)
        self.fce = {"napoveda":self.napoveda, "konec":self.konec, "nova_tk":self.nova_tk, "vsechny":self.vypis_vsechny_tridni_knihy}
        odsazeni = "\n"*(self.t_size[0]//2)
        welcome_str = "Vítejte v programu pro správu třídních knih"
        heading_str = "Autor: Štěpán Kovačič"
        print(odsazeni)
        self.print_centered_text(self.c(welcome_str, "purple"), self.c(heading_str, "green"))
        self.refresh_page(number_of_rows_to_omit=(2 +(self.t_size[0]//2) ))

    def print_centered_text(self, *text):
        for t in text:
            print(f"{t:^{self.t_size[1]}}")

    def vypis_vsechny_tridni_knihy(self):
        vsechny = manage_books.vypsat_tridni_knihy()
        maxlen = max([len(i) for i in vsechny]) + 3
        kolikrat_je_tam_dam = self.t_size[1]//maxlen
        split = [vsechny[i:i + kolikrat_je_tam_dam] for i in range(0, len(vsechny), kolikrat_je_tam_dam)]

        print("\n")
        print(f"{self.c("seznam vsech tridnickych knih", "green"):^{self.t_size[1]}}")
        print("_"*maxlen*len(split[0]))
        for i in split:
            print("".join([self.c(f"{"| " + x[:-5]:<{maxlen}}", "underline") for x in i]))
        self.refresh_page(number_of_rows_to_omit=len(split) + 2)
           

        
        # print("\n".join(["\t- " + self.c(i[:-5], "green")  for i in manage_books.vypsat_tridni_knihy()]))

    def c(self, text, color):
        #funkce se naschvál jmenuje jen c ať v kodu nezabírá moc místa 
        colors = {"purple":'\033[94m', "green":'\033[92m', "red":'\033[91m', "underline":'\033[4m'}
        return colors[color] + text + '\033[0m'
    
    def refresh_page(self, number_of_rows_to_omit=0):
        
        print("\n"*(self.t_size[0]-1 - number_of_rows_to_omit))
        Napoveda_str = "Pro nápovědu napište \"napoveda\" | Pro odchod napište \"konec\""
        print('\x1b[6;30;42m' + Napoveda_str  + (self.t_size[1]  - len(Napoveda_str)) * " " + '\033[0m')
        input_str = input("Zadejte příkaz: ")
        list_of_args = [i for i in input_str.split(" ") if i != ""]
        func_name = list_of_args[0]
        args = list_of_args[1:]
        if args != []:
            self.fce[func_name](args)
        else: self.fce[func_name]()
        

        

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

x = gui()