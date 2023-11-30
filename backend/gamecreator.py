import random as rd
import connector
from geopy import distance
import sys
import pikkufunktiot
from flask import Flask, request
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv

load_dotenv()
sqlpass = os.getenv('sqlpass')

clargs = (sys.argv)
clargs.pop(0)


#hakee yhden lentokentän ja antaa sen nimen sekä koordinaatit
def yhdenhakija(gamecountry, kursori):
    sql = "SELECT name, latitude_deg, longitude_deg FROM airport"
    sql += " WHERE (iso_country='"+gamecountry+"') AND (type='small_airport' OR type='medium_airport' OR type='large_airport')"
    # randomi order että ei ole aakkosjärjestys
    sql += " ORDER BY RAND ( )"
    sql += " LIMIT 1"
    kursori.execute(sql)
    tulos = kursori.fetchall()[0]
    return tulos

# tämä lisää tavarat sql tietokantaan
def sqlinsert(airports, kursori):
    airportid = 1
    for airportdata in airports:
        # tämä täyttää nimen, has visited ja
        # treasure chancen sekä koordinatit
        # tietokantaan
        sql = "INSERT INTO game (id, airport_name, treasure_chance, has_visited, coordinates) VALUES (%s, %s, %s, %s, %s)"
        val = (airportid, airportdata[0], airportdata[3], 0, f"({airportdata[1]}, {airportdata[2]})")
        kursori.execute(sql, val)
        airportid += 1

#tämä hakee annetun määränn lentokenttiä joiden etäisyys aloituspointista on annettu määrä.
#ekana haetaan alotuskenttä jonka avulla verrataan jos lentälentät ovat halutun kuplan sisällä
#loppulistassa jokaisella lentokoentällä on oma tuple, jossa ekana on nimi, sitten lat, lon ja vika on item prosentti
def gamemaker(kursori, limit=20, distancebetween=200):
    country = "FI"
    firstairport = yhdenhakija(country, kursori)
    firstairport = firstairport + ((rd.randint(20, 80)),)
    allaports = [firstairport]
    koordinaatit1 = firstairport[1:3]
    while len(allaports) < limit:
        fetchedairport = yhdenhakija(country, kursori)
        if fetchedairport not in allaports:
            koordinaatit2 = fetchedairport[1:3]
            pituus = (distance.distance(koordinaatit1, koordinaatit2).km)
            if pituus <= distancebetween:
                print(f"difference between {fetchedairport[0]} and {firstairport[0]} is smaller than 100km (distance: {pituus})")
                fetchedairport = fetchedairport + ((rd.randint(20, 80)),)
                allaports.append(fetchedairport)
    print(allaports)
    print(len(allaports))
    sqlinsert(allaports, kursori)
    allairportdata = []
    for airportdata in allaports:
        allairportdata.append({'name':airportdata[0], 'latitude':airportdata[1], 'longitude':airportdata[2], 'treasurechance':airportdata[3]})
    return allairportdata

if len(clargs) > 0 and clargs[0] == "run":
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    @app.route('/creategame/<limit>/<distance>')
    def creategame(limit, distance):
        yhteys = connector.sqlyhteys(sqlpass)
        kursori = yhteys.cursor()
        try:
            createdgame = gamemaker(kursori, int(limit), int(distance))
        except Exception as e:
            print(e)
            return [{'code':500, 'message':f'error "{e}" occured when creating game'}]
        return [{'code':200, 'message':'game successfully created', 'data':createdgame}]
    if __name__ == '__main__':
        app.run(use_reloader=True, host='127.0.0.1', port=3000)
else: 
    if __name__ == '__main__':
        yhteys = connector.sqlyhteys(sqlpass)
        kursori = yhteys.cursor()
        if len(clargs) > 0 and clargs[0] == "del":
            pikkufunktiot.cleardatabase(kursori)
        else:
            gamemaker(kursori)

# Tämä funktio lisää pelaajan players tietokantaan.
def player_info(id, fuel_budget, screen_name, fuel_left, yhteys):
    # Kutsutaan homebase_haku funktiota jotta saadaan
    # homebasen nimi tallenettia muuttujaan homebase
    kursori = yhteys.cursor()
    # Lisätään pelaajan tiedot players tauluun
    sql = "INSERT INTO players (id, fuel_budget, screen_name, fuel_left) VALUES (%s, %s, %s, %s, %s)"
    val = (id, fuel_budget, screen_name, fuel_left)
    kursori.execute(sql, val)
    return
