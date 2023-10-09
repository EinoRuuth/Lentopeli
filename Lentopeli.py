import connector
import gamecreator
import move
import pikkufunktiot
import sys

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
itemtons = ["8 tonnia ", "10 tonnia ", "11 tonnia ", "12 tonnia ",
            "14 tonnia ", "16 tonnia ", "18 tonnia ", "19 tonnia ",
            "20 tonnia ", " 23 tonnia "]
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
    pikkufunktiot.delete(kursori)
else:
    itemsandairports = gamecreator.airports_items(itemamount, airportamount,
                                                  itemtons, itemnames,
                                                  gamecountry, yhteys)
    gamecreator.sqlinsert(itemsandairports[0], itemsandairports[1], yhteys)
    gamecreator.player_info(id, fuel_budget, screen_name, fuel_left, yhteys)

    while True:
        lentokenttä = input("Syötä lentokenttä: ")
        if lentokenttä == "quit":
            pikkufunktiot.delete(kursori)
            exit()
        lentokenttä = pikkufunktiot.fullairportname(lentokenttä, kursori)
        move.move(lentokenttä, yhteys)
