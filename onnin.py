import connector

yhteys = connector.sqlyhteys("menat44")


def hakija( yhteys):
    sql = "SELECT airport_name FROM game"
    # randomi order että ei ole aakkosjärjestys
    sql += " ORDER BY RAND ( )"
    # limitoi etsinnät 1
    sql += " LIMIT 1 "
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos[0][0]


# tehtävä:
# tee move funktioon sille että se laittaa siihen location ton airport muuttujan
# ja katsoo polttoaineen. se returnaa true jos on polttoainetta vielä mutta jos ei ole se returnaa false
def move(airport, yhteys):
    sql = "SELECT fuel_left FROM players"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    fuel= kursori.fetchall()
    fuel = fuel[0][0]
    if fuel >= 100:
        fuelleft = fuel-100
        sql1 = "UPDATE players SET location='" + airport + "'"
        sql2 = "UPDATE players SET fuel_left='" + str(fuelleft) + "'"
        sql3 = "UPDATE game SET has_visited=%s WHERE airport_name='"+ airport + "'"
        val3 = (1,)
        kursori.execute(sql1)
        kursori.execute(sql2)
        kursori.execute(sql3,val3)
        return True
    else:
        return False


lentokenttä = hakija(yhteys)
liikkuminen = move(lentokenttä, yhteys)
if not liikkuminen:
    exit("GAMER OVER!\nYou ran out of fuel.")

#move hommma tarvii:
# lokaation päivitys player tietokantaan
# polttoaineen chekki jos ei riitä niin peli loppuu ja päivitys player tietokantaan
# treasure chekki ja sen lisäys player hommaa, ja poistaa game taulusta
# homabase chekki jos on tavara niin polttoainetta ja jos on saanut kaikki tavarat niin voittaa (pitää laskua kuinka monta arretta on viety dificultia vastaan)
# 