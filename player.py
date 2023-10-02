import random as rd
import connector

yhteys = connector.sqlyhteys("admin")

def homebase_haku(yhteys):
    sql = "SELECT airport_name FROM game"
    sql += "WHERE homebase='"+1+"'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

def player_info(players ,yhteys):
    homebase = homebase_haku()
    for playername in players:
        sql = "INSERT INTO players (id, fuel_budget, Location ,screen_name ,fuel_left ,treasures) VALUES (%s, %s, %s, %s, %s, %s)", (homebase)
        val = (playername[0], 0, 0)
        kursori = yhteys.cursor()
        kursori.execute(sql, val)
    return
