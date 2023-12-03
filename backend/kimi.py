import connector
from geopy import distance
import os
from dotenv import load_dotenv

load_dotenv()
sqlpass = os.getenv('sqlpass')
yhteys = connector.sqlyhteys(sqlpass)
kursori = yhteys.cursor()

'''
Tehtävä on tehä toi move funktio
parametrit on noi mitä on jo laitettu, eli minne ollaa menossa ja paljo polttoainetta lentoon menee

eli logiikka on sit se, et se päivittää nää tiedot player tietokantaan, ja palauttaa true/false sen mukaa toimiko vai ei
palautuksessa halutaan uuden lentokentä tiedot muodossa:
({'name':lentokentän name, 'latitude':lentokentän latitude, 'longitude':lentokentän longitude, 'treasurechance':lentokentän treasurechance})
mutta toi palautus voidaan kattoo yhes
'''


def move(kursori, targetairport, polttoaine):
    sql = "SELECT fuel_left FROM players"
    kursori.execute(sql)
    fuel = kursori.fetchall()[0][0]
    if fuel >= polttoaine:
        fuel = fuel - polttoaine
        sql2 = "UPDATE players SET location ='" + targetairport + "'"
        sql3 = "SELECT coordinates FROM game WHERE airport_name ='" + targetairport + "'"
        sql4 = "UPDATE players SET fuel_left ='" + fuel + "'"
        sql5 = "SELECT treasure_chance FROM game WHERE airport_name = '" + targetairport + "'"
        kursori.execute(sql2)
        kursori.execute(sql3)
        kursori.execute(sql4)
        kursori.execute(sql5)
        treasurechance = kursori.fetchall()[0][0]
        result = {
            'name': targetairport,
            'latitude': latitude,
            'longitude': longitude,
            'treasurechance': treasurechance
        }
    return


def start():
    sql = "SELECT airport_name FROM game"
    sql += " ORDER BY RAND ( )"
    sql += " LIMIT 1"
    yhteys = connector.sqlyhteys(sqlpass)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    airportname = kursori.fetchall()
    #
    # 
    #
    move(kursori, airportname[0][0], 1)
    print(airportname)

start()