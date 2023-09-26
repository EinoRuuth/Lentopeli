import connector
import random as rd
import sys

#config starts
#laita tähän alle oma sql salasanasi
sqlpassword="admin"
itemamount = 2
airportamount = 20
itemcolors = ["green", "blue", "red", "yellow", "white"]
itemnames = ["apple", "stick", "chair", "ball", "clock"]
#config ends

clargs = (sys.argv)
clargs.pop(0)

def hakija(limit):
    sql = "SELECT name FROM airport"
    sql += " ORDER BY RAND ( )"
    sql += " LIMIT "+str(limit)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

def airports_items(items, airports):
    airports = hakija(airports)
    allitems = []
    for number in range(items):
        itemcolor = rd.randint(0,4)
        itemname = rd.randint(0,4)
        itemfullname = itemcolors[itemcolor]+" "+itemnames[itemname]
        allitems.append(itemfullname)
    return (allitems, airports)

def sqlinsert(items, airports):
    for airportname in airports:
        sql = "INSERT INTO game (airport_name) VALUES (%s)"
        val = (airportname)
        kursori = yhteys.cursor()
        kursori.execute(sql, val)
    for itemname in items:
        itemairport = rd.randint(0,len(airports)-1)
        itemairport = airports[itemairport]
        for x in itemairport:
            itemairport=x
        sql = "UPDATE game SET treasure='"+itemname+"' WHERE airport_name='"+itemairport+"'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
    return

def delete():
    sql = "delete from game"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    print(kursori.rowcount, "record inserted.")

yhteys = connector.sqlyhteys(sqlpassword)
itemsandairports = airports_items(itemamount, airportamount)
if len(clargs) > 0 and clargs[0] == "del":
    delete()
else:
    sqlinsert(itemsandairports[0], itemsandairports[1])
