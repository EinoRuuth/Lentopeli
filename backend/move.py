import pikkufunktiot
import connector
from geopy import distance
import os
from dotenv import load_dotenv

load_dotenv()
sqlpass = os.getenv('sqlpass')
yhteys = connector.sqlyhteys(sqlpass)
kursori = yhteys.cursor()


def fuelcalc(kursori, airport1, airport2):
    sql = f"SELECT coordinates FROM game WHERE airport_name ='{airport2}'"
    kursori.execute(sql)
    coords2 = kursori.fetchall()[0][0].split(',')
    sql1 = f"SELECT coordinates FROM game WHERE airport_name ='{airport1}'"
    kursori.execute(sql1)
    coords1 = kursori.fetchall()[0][0].split(',')
    pituus = distance.distance(coords1, coords2).km

    print(pituus)

    fuel = (pituus // 50) + 1
    print(fuel)
    return {"Fuel:": fuel, 'distance': pituus}


@app.route('/move/<targetairport>/<fuelconsumption>')
def move(kursori, targetairport, fuelconsumption):
    try:
        sql = "SELECT fuel_left FROM players"
        kursori.execute(sql)
        fuelleft = kursori.fetchall()[0][0]
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
            treasurechance = kursori.fetchall()[0][0]
            kursori.execute(sql6)
            data = {'name': targetairport, 'latitude': latitude,
                    'longitude': longitude, 'tchance': treasurechance, 'fuel': fuel}
            return [{'code': 200, 'message': 'Liikuttu uudelle lentokentälle', 'moved': True, 'data': data}]
        else:
            return [{'code': 200, 'message': 'Ei voitu liikkua. Polttoaine ei riitä', 'moved': False}]
    except Exception as e:
        print(e)
        return [{'code': 500, 'message': f'error "{e}" occurred while moving'}]
