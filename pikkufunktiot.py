def fullairportname(name, kursori):
    sql = "SELECT airport_name from game WHERE airport_name LIKE '" + name + "%'"
    kursori.execute(sql)
    fullairportname = kursori.fetchall()
    if len(fullairportname):
        airport = fullairportname[0][0]
    else:
        return False
    return airport


def delete(kursori):
    sql = "delete from game"
    kursori.execute(sql)
    print(kursori.rowcount, "rows cleared.")
    sql = "delete from players"
    kursori.execute(sql)
    print(kursori.rowcount, "rows cleared.")

# pikkufunktioita jotka tarvitsen vähintään keskiviikkona saa tehä jos haluaa lisää osaa projektiin

# treasureamount funktio joka katsoo kuinka monta aarretta game taulussa lentokentissä vielä on

# fuelamount joka ottaa tietokannasta kuinka paljon polttoainetta on jäljellä

# pelaajanlokaatio eli funktio joka antaa pelaajan sen hetkisen lokaation players taulusta