import pikkufunktiot
import connector
from geopy import distance
import os
from dotenv import load_dotenv

load_dotenv()
sqlpass = os.getenv('sqlpass')
yhteys = connector.sqlyhteys(sqlpass)
kursori = yhteys.cursor()


def fuelcalc(kursori, airport1):
    returndict = {}
    sql = f"SELECT airport_name, coordinates FROM game"
    kursori.execute(sql)
    coords2 = kursori.fetchall()
    sql1 = f"SELECT coordinates FROM game WHERE airport_name ='{airport1}'"
    kursori.execute(sql1)
    coords1 = kursori.fetchall()[0][0].split(',')
    for coords in coords2:
        if coords[0] != airport1:
            secondcoords = coords[1].split(',')
            secondname = coords[0]
            pituus = distance.distance(coords1, secondcoords).km
            returndict[secondname] = (pituus // 50) + 1
    return returndict


def move(targetairport, fuelconsumption):
    sql = "SELECT fuel_left FROM players"
    kursori.execute(sql)
    fuelleft = kursori.fetchall()[0][0]
    fuelconsumption = int(fuelconsumption)
    if fuelleft >= fuelconsumption:
        fuel = fuelleft - fuelconsumption
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
        tchance = kursori.fetchall()[0][0]
        kursori.execute(sql6)
        data = {'name': targetairport, 'latitude': latitude,
                'longitude': longitude, 'tchance': tchance, 'fuel': fuel}
        return {'message': "Liikuttu uudelle lentokentälle", 'moved': True, 'data': data}
    else:
        return {'message': "Ei voitu liikkua. Polttoaine ei riitä ", 'moved': False}
