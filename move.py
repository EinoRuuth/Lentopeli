import connector

yhteys = connector.sqlyhteys("admin")


def hakija( yhteys):
    sql = "SELECT name FROM game"
    # randomi order että ei ole aakkosjärjestys
    sql += " ORDER BY RAND ( )"
    # limitoi etsinnät 1
    sql += " LIMIT "+1
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos


# tehtävä:
# tee move funktioon sille että se laittaa siihen location ton airport muuttujan
# ja katsoo polttoaineen. se returnaa true jos on polttoainetta vielä mutta jos ei ole se returnaa false
def move(airport, yhteys):
    return

polttoaineloppu = True
while polttoaineloppu:
    lentokenttä = hakija(yhteys)
    liikkuminen = move(lentokenttä, yhteys)
    if not liikkuminen:
        polttoaineloppu = False
exit("GAMER OVER!\nYou ran out of fuel.")

#move hommma tarvii:
# lokaation päivitys player tietokantaan
# polttoaineen chekki jos ei riitä niin peli loppuu ja päivitys player tietokantaan
# treasure chekki ja sen lisäys player hommaa, ja poistaa game taulusta
# homabase chekki jos on tavara niin polttoainetta ja jos on saanut kaikki tavarat niin voittaa (pitää laskua kuinka monta arretta on viety dificultia vastaan)
# 