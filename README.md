# Solderix API

Repozitorij sadrži programsku podršku i upute za SolderBIT projekte uključujuči autić i daljinski upravljač. Uz SolderBIT isto tako repozitorij sadrži micro:bit podršku za autić i daljinski upravljač bez hardvera.

# micro:bit

Kako bi se Solderix autić i daljinski upravljač osposobili na micro:bitu prvo je potrebno otići na [micro:bit Python Editor](https://python.microbit.org/v/3) web stranicu.

## micro:bit Daljinski Upravljač
Za daljinsku upravljač potrebno je prepisati programski kod iz repozitorija: ["Programski kod za daljinski upravljač"](microbit/controller/main.py). Nakon prepisivanja koda potrebno je spojiti micro:bit na računali i pritismuti tipku "Send to micro:bit" te pratiti njihove upute.
 
![alt_text](images/12345.png)

## micro:bit Autić
Za autić potrebno je skinuti i prebaciti programski kod unutar [ove mape](microbit/car) u [micro:bit Python Editor](https://python.microbit.org/v/3) pritiskom na tipku "Open". 

![alt_text](images/2345.png)

Pritiskom na "Open" otvara se pretraživać preko kojega je potrebno odabrati skinute skripte iz  [ove mape](microbit/car) u [micro:bit Python Editor](https://python.microbit.org/v/3) nakon čega je potrebno kliknuti "Confirm". Obratite pažnju da se main skripta koristi kao main.py, a vehicle.py se doda kao odvojena skripta isto kao što je prikazano na doljnoj slici.

![alt_text](images/confirm.png)

Nakon prebacivanja koda potrebno je spojiti micro:bit na računali i pritismuti tipku "Send to micro:bit" te pratiti njihove upute.
 
![alt_text](images/12345.png)

# SolderBIT

Uz kit za autić i daljinski upravljač dolazi i mikroupravljač sličan micro:bit-u. Upravljač nudi korisnicima veću programsku memoriju i bolju konfiguraciju pinova, no za razliku od micro:bit-a potrebno je uložiti malo više vremena kako bi se radno okruženje za programiranje postavilo. 

## Instalacija Python-a
Pošto SolderBIT koristi Micropython kao svoj programski jezik, potrebno je omogućiti da račualo korišteno za programiranje podržava isti. Povezica za skidanje posljednje verzije Pythona nalazi se [ovdje](https://www.python.org/downloads/). Prilikom instalacije potrebno je kliknuti na kvačicu "Add Python to PATH" kako bi se Python mogao koristiti s bilo koje lokacije na računalu. Pratiti upute unutar programa za instalaciju.

![alt_text](images/python_install.jpg)

## Instalacija Adafruit-ampy
Nakon instalacije potrebno je instalirati ampy (Adafruit MicroPYthon). Ovaj Python ekstenzija se koristi za prebacivanje napisanog koda s računala na SolderBIT. Prvo je potrebno otvoriti upravljačku konzolu operativnog sustava na računalu. Ovaj korak varira ovisno o operativnom sustavu, no uglavnom je postupak slučan. U ovom primjeru će se pokazati kako se to radi na Windows 11. Potrebno je pritisnuti na Windows Start ikonu te u pretraživać utipkati "Terminal" ili "Powershell".

![alt_text](images/terminal.png)

Otvara se crni prozor unutar kojega je potrebno upisati sljedeću liniju:

```
pip install adafruit-ampy
```

Pričekati da se instalira. U slučaju da je potrebno više informacije vezano uz adafruit-ampy kliknuti na sljedeći [link](https://pypi.org/project/adafruit-ampy/).

## Pisanje koda
Kao što je već navedeno, kod se piše u Python-u. Sav programski kod za autić u daljinski upravljač moguće je pronaći u repozitoriju na ovom [linku](solderbit). Kako bi napisali vlastiti kod potrebno je napraviti datoteku `main.py` te unutar nje napisati željeni kod. Sintaxa pisanja identična je Micropythonu za micro:bit uz par izuzetaka. Pisanje programskog koda se vrši u uređivači teksta po izboru (VS Code, Notepad, Notepad++, .






