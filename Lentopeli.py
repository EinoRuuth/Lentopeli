import connector
import random as rd

#config starts
sqlpassword="admin"
itemamount = 2
airportamount = 2
#config ends

color = ["green", "blue", "red", "yellow", "white"]
item = ["apple", "stick", "chair", "ball", "clock"]
items = []

def hakija(limit):
    sql = "SELECT name FROM airport"
    sql += " ORDER BY RAND ( )"
    sql += " LIMIT "+str(limit)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    if kursori.rowcount >0 :
        print(tulos)
    return

# laita allaolevaan sulkujen sisään oman salasanasi
yhteys = connector.sqlyhteys(sqlpassword)

hakija(airportamount)
for number in range(itemamount):
    itemcolor = rd.randint(0,4)
    itemname = rd.randint(0,4)
    itemfullname = color[itemcolor]+" "+item[itemname]
    items.append(itemfullname)

print(items)
