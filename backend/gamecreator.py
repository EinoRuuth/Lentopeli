import random as rd
import connector
from geopy import distance
import sys
import pikkufunktiot
from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()
sqlpass = os.getenv('sqlpass')
yhteys = connector.sqlyhteys(sqlpass)
kursori = yhteys.cursor()

clargs = (sys.argv)
clargs.pop(0)

alotuskentat = ['Oulu Airport',
                'Kuopio Airport',
                'Jyväskylä Airport',
                'Parkano Airfield',
                'Räyskälä Airfield',
                'Viitasaari Airfield',
                'Haapavesi Airfield',
                'Ilvesjoki UL',
                'Lahti Vesivehmaa Airport',
                'Mikkeli Airport']

startports = ['Randys Airpark',
              'McAllister Wash Airstrip',
              'Tragesser Airport',
              'Hazlehurst Airport',
              'Matzie Airport',
              'Powhatan Airport',
              'Rohnerville Airport',
              'Park Township Airport',
              'Rohwer Airport']

#hakee yhden lentokentän ja antaa sen nimen sekä koordinaatit
def yhdenhakija(gamecountry, kursori):
    sql = "SELECT name, latitude_deg, longitude_deg FROM airport"
    sql += " WHERE (iso_country='"+gamecountry+"') AND (type='small_airport' OR type='medium_airport' OR type='large_airport')"
    # randomi order että ei ole aakkosjärjestys
    sql += " ORDER BY RAND ( )"
    sql += " LIMIT 1"
    kursori.execute(sql)
    tulos = kursori.fetchall()[0]
    if "'" in tulos[0]:
        yhdenhakija(gamecountry, kursori)
    return tulos

# tämä lisää tavarat sql tietokantaan
def sqlinsert(airports, kursori):
    airportid = 1
    first = 0
    for airportdata in airports:
        # tämä täyttää nimen, has visited ja
        # treasure chancen sekä koordinatit
        # tietokantaan
        if first == 0:
            visited = 1
        else:
            visited = 0
        sql = "INSERT INTO game (id, airport_name, treasure_chance, has_visited, coordinates) VALUES (%s, %s, %s, %s, %s)"
        val = (airportid, airportdata[0], airportdata[3], visited, f"{airportdata[1]}, {airportdata[2]}")
        kursori.execute(sql, val)
        first += 1
        airportid += 1

# Tämä funktio lisää pelaajan players tietokantaan.
def player_info(kursori, location, id, fuel_budget, screen_name):
    sql = "INSERT INTO players (id, fuel_budget, location, fuel_left, screen_name) VALUES (%s, %s, %s, %s, %s)"
    val = (id, fuel_budget, location, fuel_budget, screen_name)
    kursori.execute(sql, val)
    return

def startingport(country):
    if country == "FI":
        startingport = rd.choice(alotuskentat)
        sql = "SELECT name, latitude_deg, longitude_deg FROM airport"
        sql += f" WHERE name='{startingport}' AND (type='small_airport' OR type='medium_airport' OR type='large_airport')"
        sql += " ORDER BY RAND ( )"
        sql += " LIMIT 1"
        kursori.execute(sql)
        firstairportreturn = kursori.fetchall()[0]
        return firstairportreturn
    else:
        startingport = rd.choice(startports)
        sql = "SELECT name, latitude_deg, longitude_deg FROM airport"
        sql += f" WHERE name='{startingport}' AND (type='small_airport' OR type='medium_airport' OR type='large_airport')"
        sql += " ORDER BY RAND ( )"
        sql += " LIMIT 1"
        kursori.execute(sql)
        firstairportreturn = kursori.fetchall()[0]
        if "'" in firstairportreturn[0]:
            startingport(country)
        return firstairportreturn

#tämä hakee annetun määränn lentokenttiä joiden etäisyys aloituspointista on annettu määrä.
#ekana haetaan alotuskenttä jonka avulla verrataan jos lentälentät ovat halutun kuplan sisällä
#loppulistassa jokaisella lentokoentällä on oma tuple, jossa ekana on nimi, sitten lat, lon ja vika on item prosentti
def gamemaker(kursori, country, limit=20, distancebetween=200):
    firstairport = startingport(country)
    print(firstairport)
    allaports = [firstairport]
    koordinaatit1 = firstairport[1:3]
    while len(allaports) < limit:
        fetchedairport = yhdenhakija(country, kursori)
        if fetchedairport not in allaports:
            koordinaatit2 = fetchedairport[1:3]
            pituus = (distance.distance(koordinaatit1, koordinaatit2).km)
            if pituus <= distancebetween:
                print(f"difference between {fetchedairport[0]} and {firstairport[0]} is smaller than {pituus}km (distance: {pituus})")
                allaports.append(fetchedairport)
    for portnumber in range(len(allaports)):
        allaports[portnumber] = allaports[portnumber] + ((rd.randint(20, 80)),)
    print(allaports)
    print(len(allaports))
    sqlinsert(allaports, kursori)
    allairportdata = []
    for airportdata in allaports:
        allairportdata.append({'name':airportdata[0], 'latitude':airportdata[1], 'longitude':airportdata[2], 'treasurechance':airportdata[3]})
    return allairportdata
