# Instrukcja obsługi
Wszystkie pliki powinny znajdować się w AGHSolarPlane\Amperomierz.
## 1. Uruchomienie wirtualnego portu
1. Otworzyć **Wiersz Poleceń** i przejść do  folderu hub4com w Amperomierzu (cd nazwa_folderu)
2. Wykonać polecenie
```commandline
hub4com.exe --octs=off --baud=57600\\.\COM12 \\.\CNCA0 \\.\CNCA1
```
Nie zamykać okna z tym wierszem polecenia, inaczej przestaną działać i program od amperomierza, i Mission Planner!
## 2. Uruchomienie Mission Planner
Tak jak normalnie, ale wybrany port to musi być COM14.
## 3. Uruchomienie AmmeterModule
1. Otworzyć drugi **Wiersz Poleceń** i przejść do  folderu Amperomierz\env\Scripts
2. Wykonać polecenie
```commandline
activate.bat
```
Przed aktualnym folderem w wierszu poleceń powinnno się teraz wyświetlać 'env'.
3. Przejśc do folderu Amperomierz\AmmeterModule (cofanie się to cd ..)
4. Wykonać polecenie
```commandline
python main.py --port COM15
```