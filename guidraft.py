import manage_books
import os

class Gui:
    def __init__(self):
        # Get terminal size for output formatting
        self.t_size = os.get_terminal_size()
        
        # Print a welcome message
        print("\n" * (self.t_size.lines // 2))
        print("Vítejte v programu pro správu třídních knih".center(self.t_size.columns))
        print("Autor: Štěpán Kovačič".center(self.t_size.columns))
        
        # Start the command loop
        self.command_loop()

    def command_loop(self):
        while True:
            print("\nPro nápovědu napište 'napoveda' | Pro odchod napište 'konec'")
            user_input = input("Zadejte příkaz: ").strip()
            
            if user_input == "napoveda":
                self.show_help()
            elif user_input == "konec":
                self.exit_program()
            elif user_input == "vsechny":
                self.show_all_books()
            elif user_input.startswith("nova_tk"):
                self.create_class_book(user_input.split()[1:])
            else:
                print("Neplatný příkaz, zadejte 'napoveda' pro nápovědu.")
    
    def show_help(self):
        print("""
        Nápověda pro program na správu třídnických knih:
        > nova_tk <jméno třídy> <křestní jm. t.u.> <prijimeni t.u.> - Vytvoření nové třídní knihy
        > vsechny - Zobrazení všech třídních knih
        > konec - Ukončení programu
        """)
    
    def show_all_books(self):
        books = manage_books.vypsat_tridni_knihy()
        if books:
            print("\nSeznam všech třídních knih:")
            for book in books:
                print(f"- {book[:-5]}")
        else:
            print("Žádné třídní knihy nejsou k dispozici.")
    
    def create_class_book(self, args):
        if len(args) == 3:
            manage_books.vytvorit_tridni_knihu(*args)
            print("Nová třídní kniha byla vytvořena.")
        else:
            print("Neplatné argumenty pro příkaz nova_tk.")
    
    def exit_program(self):
        print("Program ukončen.")
        exit()

# Run the simplified GUI
Gui()
