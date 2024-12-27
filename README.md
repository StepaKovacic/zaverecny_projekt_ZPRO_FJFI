# Program pro správu třídnických knih

## Zapnutí
Při zapnutí programu se Vám objeví první dialog, který požaduje veliksot terminálového okna. Tomuto dialogu by se šlo vyhnout pomocí následujícího kódu, který však využívá knihovnu `os`, která není povolená. 
```python
import os
print(os.get_terminal_size())
```

V případě Linux / Mac to zjistíte pomocí tohoto příkazu
```bash
echo "Do inicializačního řádku programeu napište [`tput lines` `tput cols`] (bez závorek)"
```

Alternativa pro Windows je 
```powershell
$size = $Host.UI.RawUI.WindowSize; " Do inicializačního řádku programeu napište [$($size.Height) $($size.Width)] (bez závorek)"
```
## Architektura programu
Projekt se skládá z několika souborů 
- `main.py`, který obsahuje spouštěcí funkce a metody separátních částí projektu
- `config.py` obsahující předdefinované struktury JSON a některé globální proměnné
- `gui.py` obsahující třídu uživatelského rozhraní
- `manage_books.py` obsahuje funkce, metody a třídy pro uprávu, načítání a operace s třídnickými knihami
- složka `/tridnicke_knihy`ve které jsou ukládány jak třídnické knihy ve formátu `.json` tak soubor s unikátními `usernames`
