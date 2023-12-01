import pikkufunktiot
import connector
from geopy import distance


def lentokentta(kursori, airport1, airport2):
    sql = "SELECT * FROM game WHERE airport_name =" + airport2 
    kursori.execute(sql)
    lentokentta1 = kursori.fetchall()[0]
    sql1 = "SELECT coordinates FROM game WHERE airport_name =" + airport1
    kursori.execute(sql1)
    airport1_coords = kursori.fetchall()[0][0]
    coords2 = airport2['coordinates']
    pituus = distance.distance(airport1_coords, coords2).km

    if pituus <= 50:
        fuel_amount = 1
    elif pituus <= 100:
        fuel_amount = 2

    print("Fuel amount needed:", fuel_amount)
    return pituus
    
    
 



if __name__ == "__main__":
    sql = "SELECT airport_name FROM game"
    sql += " ORDER BY RAND ( )"
    sql += " LIMIT 2"
    yhteys = connector.sqlyhteys("admin")
    kursori = yhteys.cursor()
    kursori.execute(sql)
    airportname = kursori.fetchall()
    #
    # 
    #
    lentokentta(kursori, airportname[0], airportname[1])
    print(airportname)
'''
tehtävää varten runaa UUSI gamecreator file yksinään jotta saat täytettyä tietokannan

eli tehtävä on semmone:
sulla on toi move funktio, se pitää muuttaa sillee, että se ottaa sisään kaks lentokenttää, 
toinen se missä pelaaja on ja toinen se minne pelaaja haluaa mennä.
sitten se etsii MEIDÄN tietokannasta sen lentokentän tiedot johon halutaan liikkua.
sitten se laittaa kaikki tiedot uudesta lentokentästä dictionaryyn.

lopuksi sitten sinun pitää laittaa liikkumisen polttoaine määrä mukaan. 
eli vertaat nykyisen ja uuden lentokentän välin pituuden ja jos se matka on 0-50km fuel määrä on 1 jos 
pituus on 50-100km sit fuel määrä on 2 ja niin eteenpäin.
'''