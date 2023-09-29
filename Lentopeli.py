import connector
import gamecreator
import random as rd
import sys

#config starts
#laita tähän alle oma sql salasanasi
sqlpassword="admin"
gamecountry = "FI"
itemamount = 2
airportamount = 20
itemtons = ["8 tonnia ", "11.5 tonnia ", "13 tonnia ", "15 tonnia ", "16 tonnia "]
itemnames = ["aurinkopaneeleita", "stick", "chair", "ball", "clock"]
#config ends

clargs = (sys.argv)
clargs.pop(0)

def delete():
    sql = "delete from game"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    print(kursori.rowcount, "rows cleared.")

yhteys = connector.sqlyhteys(sqlpassword)
itemsandairports = gamecreator.airports_items(itemamount, airportamount, itemtons, itemnames, gamecountry, yhteys)
if len(clargs) > 0 and clargs[0] == "del":
    delete()
else:
    gamecreator.sqlinsert(itemsandairports[0], itemsandairports[1], yhteys)
