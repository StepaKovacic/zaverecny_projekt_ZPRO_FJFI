# Program pro správu třídnických knih

## Zapnutí
Při zapnutí programu se Vám objeví první dialog, který požaduje veliksot terminálového okna. 

V případě Linux / Mac to zjistíte pomocí tohoto příkazu
```bash
echo "Do inicializačního řádku progremeu napište [`tput lines` `tput cols`] (bez závorek)"
```

Alternativa pro Windows je 
```powershell
$size = $Host.UI.RawUI.WindowSize; " Do inicializačního řádku progremeu napište [$($size.Height) $($size.Width)] (bez závorek)"
```
