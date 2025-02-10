# Program pro správu třídnických knih
Zapnutí probíhá pomocí `main.py`, poté stačí napsat `napoveda` a rozbalí se nabídka příkazů. 


# Struktura

Projekt se skládá z několika souborů

- `main.py`, který obsahuje spouštěcí funkci programu
- `config.py` obsahující předdefinované struktury JSON a některé globální proměnné
- `gui.py` obsahující třídu uživatelského rozhraní
- `manage_books.py` obsahuje funkce, metody a třídy pro uprávu, načítání a operace s třídnickými knihami
- složka `/tridni_knihy`ve které jsou ukládány jak třídnické knihy ve formátu `.json` tak soubor s unikátními `usernames`

# Důležité

Je potřeba změnit základní cestu `GLOBAL_LOCATION = "/Users/stepankovacic/skola/code/zaverecny_projekt_ZPRO_FJFI/tridni_knihy/"` v `config.py` na vlastní cestu.
