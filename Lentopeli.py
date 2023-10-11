import connector
import gamecreator
import move
import pikkufunktiot
import sys
import time

clargs = (sys.argv)
clargs.pop(0)

# config starts
# laita tähän alle oma sql salasanasi
sqlpassword = "admin"
# lentokenttien maa
gamecountry = "FI"
# pelin vaikeustason config
difficulty = "helppo"
if difficulty == "helppo":
    itemamount = 2
    airportamount = 20
elif difficulty == "vaativa":
    itemamount = 5
    airportamount = 50
else:
    itemamount = 10
    airportamount = 100
# tavaroitten määrät ja nimet
itemtons = ["8 tonnia", "10 tonnia", "11 tonnia", "12 tonnia",
            "14 tonnia", "16 tonnia", "18 tonnia", "19 tonnia",
            "20 tonnia", "23 tonnia"]
itemnames = ["aurinkopaneeleita", "puutavaraa", "teräslevyjä",
             "sähkölaitteita", "tekstiileitä", "säilykkeitä",
             "työkaluja", "postia", "rakennustarvikkeita",
             "koneiden varaosia"]
# Playerin tiedot
id = 1
fuel_budget = 1000
screen_name = "player"
fuel_left = 1000
treasures = 0
# config ends


yhteys = connector.sqlyhteys(sqlpassword)
kursori = yhteys.cursor()
if len(clargs) > 0 and clargs[0] == "del":
    pikkufunktiot.cleardatabase(kursori)
else:
    difficulty = input("Mikä vaikeustaso?(helppo)(keskitaso)(vaikea): ")
    if difficulty == "keskitaso":
        itemamount = 5
        airportamount = 50
    elif difficulty == "vaikea":
        itemamount = 10
        airportamount = 100
    else:
        itemamount = 2
        airportamount = 20
    itemsandairports = gamecreator.airports_items(itemamount, airportamount,
                                                  itemtons, itemnames,
                                                  gamecountry, yhteys)
    gamecreator.sqlinsert(itemsandairports[0], itemsandairports[1], yhteys)
    gamecreator.player_info(id, fuel_budget, screen_name, fuel_left, yhteys)

    homebasename = gamecreator.homebase_haku(kursori)
    notvisitedairport = gamecreator.airportsearch(kursori)
    for airportname in range(len(notvisitedairport)):
        notvisitedairport[airportname] = notvisitedairport[airportname][0]
    notvisitedairport.remove(homebasename)
    notvisitedairport.sort()

    while True:
        treasureamountleft = pikkufunktiot.treasureamount(kursori)
        fuelamountleft = pikkufunktiot.fuelamount(kursori)
        lokaatio = pikkufunktiot.playerlocation(kursori)
        if fuelamountleft == 0:
            print(f"GAME OVER! Polttoaineesi loppu")
            pikkufunktiot.cleardatabase(kursori)
            exit()
        print(f"Tämänhetkinen lokaato: {lokaatio}")
        print(f"Jäljellä olevaa rahtia: {treasureamountleft}")
        print(f"Polttoainetta jäljellä: {fuelamountleft}")
        print(f"Kotikenttäsi nimi on: {homebasename}")
        print(f"Lentokenttiä joilla et ole vielä käynyt: {notvisitedairport}")
        lentokenttä = input("mihin lentokenttään haluaisi liikkua?(quit lopettaa): ")
        if lentokenttä == "quit":
            pikkufunktiot.cleardatabase(kursori)
            exit("Lopetit pelin")
        lentokenttä = pikkufunktiot.fullairportname(lentokenttä, kursori)
        if lentokenttä not in notvisitedairport and lentokenttä != homebasename:
            print("Lentokenttää ei tunnistettu")
            time.sleep(0.5)
            print()
            continue
        move.move(lentokenttä, yhteys)
        if lentokenttä in notvisitedairport:
            notvisitedairport.remove(lentokenttä)
        print()
