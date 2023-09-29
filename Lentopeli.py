import connector
import gamecreator
import random as rd
import sys

clargs = (sys.argv)
clargs.pop(0)

if len(clargs) > 0:
    sqlpassword=clargs[0]

#config starts
#laita tähän alle oma sql salasanasi
gamecountry = "FI"
itemamount = 2
airportamount = 20
itemtons = ["8 tonnia ", "11.5 tonnia ", "13 tonnia ", "15 tonnia ", "16 tonnia "]
itemnames = ["aurinkopaneeleita", "stick", "chair", "ball", "clock"]
#config ends

def delete():
    sql = "delete from game"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    print(kursori.rowcount, "rows cleared.")

yhteys = connector.sqlyhteys(sqlpassword)
itemsandairports = gamecreator.airports_items(itemamount, airportamount, itemtons, itemnames, gamecountry, yhteys)
if len(clargs) > 1 and clargs[1] == "del":
    delete()
else:
    gamecreator.sqlinsert(itemsandairports[0], itemsandairports[1], yhteys)
