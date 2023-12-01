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

def move(kursor, targetairport, polttoaine):
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