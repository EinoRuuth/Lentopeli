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

    fuel = (pituus // 50)+1
    print(fuel)
    return {"Fuel amount:": fuel}
