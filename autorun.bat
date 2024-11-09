@echo off

:: Parameterek bekerese a felhasznalotol
set /p count=Add meg, hany jatekot futassunk: 
set /p p1=Add meg az elso jatekosprofilt (p1): 
set /p p2=Add meg a masodik jatekosprofilt (p2): 

:: Elore beallitott parameterek
set mode=cvc

:: Ciklus a parancs lefuttatasahoz
for /L %%i in (1,1,%count%) do (
    echo Futtatas szama %%i
    python main.py --debug --mode %mode% --p1 %p1% --p2 %p2% --log
)

echo Kesz!
pause
