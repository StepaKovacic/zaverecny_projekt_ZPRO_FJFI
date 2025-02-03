import manage_books
import os

class Gui:
    def __init__(self):
        self.t_size = os.get_terminal_size()
        self.fce = {"napoveda": self.napoveda, "konec": self.konec, "nova_tk": self.nova_tk, "vsechny": self.vypis_vsechny_tridni_knihy}
        self.print_centered("Vítejte v programu pro správu třídních knih", "Autor: Štěpán Kovačič")
        self.refresh_page()

    def print_centered(self, *texts):
        for text in texts:
            print(f"{text:^{self.t_size.columns}}")

    def vypis_vsechny_tridni_knihy(self):
        vsechny = manage_books.vypsat_tridni_knihy()
        maxlen = max(len(i) for i in vsechny) + 3
        split = [vsechny[i:i + self.t_size.columns // maxlen] for i in range(0, len(vsechny), self.t_size.columns // maxlen)]

        print(f"{self.c('Seznam všech třídních knih', 'green'):^{self.t_size.columns}}")
        print("_" * maxlen * len(split[0]))
        for row in split:
            print("".join([self.c(f"| {x[:-5]:<{maxlen}}", "underline") for x in row]))
        self.refresh_page(len(split) + 2)

    def c(self, text, color):
        colors = {"purple": '\033[94m', "green": '\033[92m', "red": '\033[91m', "underline": '\033[4m'}
        return colors[color] + text + '\033[0m'

    def refresh_page(self, rows_to_omit=0):
        print("\n" * (self.t_size.lines - rows_to_omit - 1))
        print('\x1b[6;30;42m' + "Pro nápovědu napište 'napoveda' | Pro odchod napište 'konec'" + (self.t_size.columns - 44) * " " + '\033[0m')
        input_str = input("Zadejte příkaz: ")
        list_of_args = input_str.split()
        func_name = list_of_args[0]
        args = list_of_args[1:]
        if args:
            self.fce[func_name](args)
        else:
            self.fce[func_name]()

    def konec(self):
        print("\n" * (self.t_size.lines - 1))
        print(self.c("Program ukončen", "green"))

    def napoveda(self):
        napoveda_string = """
        Nápověda:
        > [nova_tk <třída> <jm. t.u.>] Vytvoří novou třídní knihu
        > [zobraz_tk <třída>] Zobrazí třídní knihu
        > [konec] Ukončí program
        """
        print(napoveda_string)
        self.refresh_page(len(napoveda_string.split("\n")))

    def nova_tk(self, args):
        manage_books.vytvorit_tridni_knihu(*args)
        self.vypis_vsechny_tridni_knihy()

x = Gui()
