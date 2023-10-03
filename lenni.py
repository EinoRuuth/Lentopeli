import connector

yhteys = connector.sqlyhteys("admin")


def hakija(limit, yhteys):
    sql = "SELECT airport_name FROM game"
    # randomi order että ei ole aakkosjärjestys
    sql += " ORDER BY RAND ( )"
    # limitoi etsinnät 1
    sql += " LIMIT "+str(limit)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

limit = 1
lentokenttä = hakija(limit, yhteys)
def treasure_haku(tavarat, yhteys):
    lentokentan_nimi = tavarat[0][0]
    sql = "SELECT treasure FROM game"
    sql += " WHERE (airport_name='"+lentokentan_nimi+"')"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    aarre = kursori.fetchall()
    return aarre


aarre = treasure_haku(lentokenttä, yhteys)


def treasure_check(aarre, tavarat, yhteys):
    lentokentan_nimi = tavarat[0][0]
    merkkijono = ""
    if aarre[0][0]:
        sql = "UPDATE players SET treasures='"+aarre[0][0]+"' WHERE id='"+"1"+"'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        merkkijono = (f"{lentokentan_nimi}ssä on aarre. Aarre lisätty ruumaan")
    else:
        merkkijono = (f"{lentokentan_nimi}ssä ei ole aarretta")
    return merkkijono

print(treasure_check(aarre, lentokenttä, yhteys))

#move hommma tarvii:
# lokaation päivitys player tietokantaan
# polttoaineen chekki jos ei riitä niin peli loppuu ja päivitys player tietokantaan
# treasure chekki ja sen lisäys player hommaa, ja poistaa game taulusta
# homabase chekki jos on tavara niin polttoainetta ja jos on saanut kaikki tavarat niin voittaa (pitää laskua kuinka monta arretta on viety dificultia vastaan)
