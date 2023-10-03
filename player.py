def homebase_haku(yhteys):
    sql = "SELECT airport_name FROM game WHERE homebase=1"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos[0][0]

def player_info(id, fuel_budget, screen_name, fuel_left, yhteys):
    homebase = homebase_haku(yhteys)
    sql = "INSERT INTO players (id, fuel_budget, Location, screen_name, fuel_left) VALUES (%s, %s, %s, %s, %s)"
    val = (id, fuel_budget, homebase, screen_name, fuel_left)
    kursori = yhteys.cursor()
    kursori.execute(sql, val)
    return