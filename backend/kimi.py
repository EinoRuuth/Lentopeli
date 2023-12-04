import connector
from geopy import distance
import os
from dotenv import load_dotenv
import gamecreator
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
    fuelleft = kursori.fetchall()[0][0]
    if fuelleft >= polttoaine:
        fuel = fuelleft - polttoaine
        sql2 = f"UPDATE players SET location ='" + targetairport + "'"
        sql3 = f"SELECT coordinates FROM game WHERE airport_name ='{targetairport}'"
        sql4 = f"UPDATE players SET fuel_left ='{fuel}'"
        sql5 = f"SELECT treasure_chance FROM game WHERE airport_name ='{targetairport}'"
        sql6 = f"UPDATE game SET has_visited=1 WHERE airport_name ='{targetairport}'"
        kursori.execute(sql2)
        kursori.execute(sql3)
        latitude, longitude = kursori.fetchall()[0][0].split(',')
        kursori.execute(sql4)
        kursori.execute(sql5)
        treasurechance = kursori.fetchall()[0][0]
        kursori.execute(sql6)
        data = {'name': targetairport, 'latitude': latitude,
                'longitude': longitude, 'treasure chance': treasurechance}
        message = "Liikuttu uudelle lentokentälle."
        return True, data, message
    else:
        message = "Ei voitu liikkua. Polttoaine ei riitä."
        return False, message


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