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
    lentokoneen_polttoaine = yhteys['fuel_left']
    nykyinen_sijainti = yhteys['location']
    polttoaineen_kulutus_per_lento = yhteys['fuel_budget']
    etaisyys = abs(nykyinen_sijainti - airport)
    tarvittava_polttoaine = etaisyys * polttoaineen_kulutus_per_lento

    if lentokoneen_polttoaine >= tarvittava_polttoaine:
        yhteys['fuel_budget'] -= tarvittava_polttoaine
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