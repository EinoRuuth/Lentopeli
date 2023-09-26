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
itemcolors = ["green", "blue", "red", "yellow", "white"]
itemnames = ["apple", "stick", "chair", "ball", "clock"]
#config ends

clargs = (sys.argv)
clargs.pop(0)

def delete():
    sql = "delete from game"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    print(kursori.rowcount, "rows cleared.")

yhteys = connector.sqlyhteys(sqlpassword)
itemsandairports = gamecreator.airports_items(itemamount, airportamount, itemcolors, itemnames, gamecountry)
if len(clargs) > 0 and clargs[0] == "del":
    delete()
else:
    gamecreator.sqlinsert(itemsandairports[0], itemsandairports[1])
