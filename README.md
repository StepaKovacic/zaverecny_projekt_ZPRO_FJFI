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
