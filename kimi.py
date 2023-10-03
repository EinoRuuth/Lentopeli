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

# tehtävä2:
# tehtävä on kattoo onko lentokentällä arretta, jos siel on niin se laittaa sen player tietokanna treasure kohtaan
# ja poistaa sen sieltä game taulusta sekä returnaa on true
# jos ei ole niin se returnaa false
def treasure(airport, yhteys):
    return


lentokenttä = hakija(yhteys)
treasure(lentokenttä, yhteys)


#move hommma tarvii:
# lokaation päivitys player tietokantaan
# polttoaineen chekki jos ei riitä niin peli loppuu ja päivitys player tietokantaan
# treasure chekki ja sen lisäys player hommaa, ja poistaa game taulusta
# homabase chekki jos on tavara niin polttoainetta ja jos on saanut kaikki tavarat niin voittaa (pitää laskua kuinka monta arretta on viety dificultia vastaan)
# 