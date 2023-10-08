import connector

yhteys = connector.sqlyhteys("admin!")


def hakija(yhteys):
    sql = "SELECT airport_name FROM game"
    # randomi order että ei ole aakkosjärjestys
    sql += " WHERE homebase='1'"
    sql += " ORDER BY RAND ( )"
    # limitoi etsinnät 1
    sql += " LIMIT 1"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos[0][0]

# tehtävä:
# tehtävä on tehdä homebase chekki eli jos henkilö on liikkunut lentokentälle joka on homebase pitää katsoa jos pelaajalla on aarre
# jos pelaajalla on aarre otetaan se siltä pois ja annetaan täydet polttoaineet
# ja sit JOS ON MAHDOLLISTA JA OSAAT tee semmonen chekki joka katsoo jos aarteita on vielä jäljellä, ja jos ei ole se lopettaa pelin. (JOS et osaa niin joko eino tai lenni tekee)
def homebasecheck(airport, yhteys):
    sql = "SELECT homebase FROM game"
    sql += " WHERE (airport_name='"+airport+"')"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    homebase = kursori.fetchall()
    if len(homebase) != 0:
        sql1 = "SELECT treasures FROM players"
        kursori = yhteys.cursor()
        kursori.execute(sql1)
        treasure = kursori.fetchall()
        if treasure != "(NULL)":
            sql2 = "UPDATE players SET treasures = '(NULL)'"
            kursori = yhteys.cursor()
            kursori.execute(sql2)
            sql3 = "UPDATE players SET fuel_left= 1000"
            kursori = yhteys.cursor()
            kursori.execute(sql3)
    return


lentokenttä = hakija(yhteys)
homebasecheck(lentokenttä, yhteys)


#move hommma tarvii:
# lokaation päivitys player tietokantaan
# polttoaineen chekki jos ei riitä niin peli loppuu ja päivitys player tietokantaan
# treasure chekki ja sen lisäys player hommaa, ja poistaa game taulusta
# homabase chekki jos on tavara niin polttoainetta ja jos on saanut kaikki tavarat niin voittaa (pitää laskua kuinka monta arretta on viety dificultia vastaan)
# 