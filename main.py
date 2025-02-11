from gui import Gui 
import os 
from config import GLOBAL_LOCATION


if __name__ == "__main__":

    print(GLOBAL_LOCATION)
    if os.path.isfile(GLOBAL_LOCATION + "all_students.json"):
        gui = Gui()

    else:
        print("\033[91m\tNastala chyba, soubor all_students.json nebyl nalezen.\033[0m")
        

