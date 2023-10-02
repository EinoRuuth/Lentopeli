import connector
import gamecreator
import random as rd
import sys

clargs = (sys.argv)
clargs.pop(0)


#config starts
#laita tähän alle oma sql salasanasi
sqlpassword="admin"
gamecountry = "FI"
itemamount = 2
airportamount = 20
itemtons = ["8 tonnia ", "10 tonnia ", "11 tonnia ", "12 tonnia ", "14 tonnia ", "16 tonnia ", "18 tonnia ", "19 tonnia ", "20 tonnia ", " 23 tonnia "]
itemnames = ["aurinkopaneeleita", "puutavaraa", "teräslevyjä", "sähkölaitteita", "tekstiileitä", "säilykkeitä", "työkaluja", "postia", "rakennustarvikkeita", "koneiden varaosia"]
#Playerin tiedot
id = 1 
fuel_budget = 1000
screen_name = "player"
fuel_left = 1000
treasures = 0
#config ends

def delete():
    sql = "delete from game"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    print(kursori.rowcount, "rows cleared.")
    sql = "delete from players"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    print(kursori.rowcount, "rows cleared.")

yhteys = connector.sqlyhteys(sqlpassword)
if len(clargs) > 0 and clargs[0] == "del":
    delete()
else:
    itemsandairports = gamecreator.airports_items(itemamount, airportamount, itemtons, itemnames, gamecountry, yhteys)
    gamecreator.sqlinsert(itemsandairports[0], itemsandairports[1], yhteys)
