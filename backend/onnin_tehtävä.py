import pikkufunktiot
import connector

def move(airport, yhteys):
    sql = "SELECT fuel_left FROM players"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    fuel = kursori.fetchall()[0][0]
    if fuel >= 100:
        fuelleft = fuel-100
        sql1 = "UPDATE players SET location='" + airport + "'"
        sql2 = "UPDATE players SET fuel_left='" + str(fuelleft) + "'"
        sql3 = "UPDATE game SET has_visited=%s WHERE airport_name='"+ airport + "'"
        val3 = (1,)
        kursori.execute(sql1)
        kursori.execute(sql2)
        kursori.execute(sql3,val3)
        print(f"Olet liikkunut {airport}ille")
        return
    else:
        print("Peli ohi! Polttoaineesi loppui.")
        pikkufunktiot.cleardatabase(kursori)
        exit()
        
if __name__ == "__main__":
    sql = "SELECT airport_name FROM game"
    sql += " ORDER BY RAND ( )"
    sql += " LIMIT 2"
    yhteys = connector.sqlyhteys("admin")
    kursori = yhteys.cursor()
    kursori.execute(sql)
    airportname = kursori.fetchall()
    #
    # ONNI TÄSSÄ ALLA ANNAN SUN FUNKTIOON TAVARAT eli ekana on yhteys, sit on airport jossa pelaaja on ja sit lentokenttä johon halutaa liikkua
    #
    move(yhteys, airportname[0], airportname[1])
    print(airportname)
        
'''
tehtävää varten runaa UUSI gamecreator file yksinään jotta saat täytettyä tietokannan

eli tehtävä on semmone:
sulla on toi move funktio, se pitää muuttaa sillee, että se ottaa sisään kaks lentokenttää, toinen se missä pelaaja on ja toinen se minne pelaaja haluaa mennä.
sitten se etsii MEIDÄN tietokannasta sen lentokentän tiedot johon halutaan liikkua.
sitten se laittaa kaikki tiedot uudesta lentokentästä dictionaryyn.

lopuksi sitten sinun pitää laittaa liikkumisen polttoaine määrä mukaan. 
eli vertaat nykyisen ja uuden lentokentän välin pituuden ja jos se matka on 0-50km fuel määrä on 1 jos pituus on 50-100km sit fuel määrä on 2 ja niin eteenpäin.
'''