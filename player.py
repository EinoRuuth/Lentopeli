import random as rd
import connector
import sys
import Lentopeli

clargs = (sys.argv)
print(clargs)
yhteys = connector.sqlyhteys("1234")

id = 1 
fuel_budget = 1000
screen_name = "player"
fuel_left = 1000
treasures = 0

def homebase_haku(yhteys):
    sql = "SELECT airport_name FROM game"
    sql += "WHERE homebase='1'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

def player_info(id, fuel_budget, screen_name, fuel_left, yhteys):
    homebase = homebase_haku(yhteys)
    sql = "INSERT INTO players (id, fuel_budget, Location, screen_name, fuel_left) VALUES (%s, %s, %s, %s, %s)"
    val = (id, fuel_budget, screen_name, homebase, fuel_left)
    kursori = yhteys.cursor()
    kursori.execute(sql, val)
    return

if len(clargs) > 0 and clargs[0] == "del":
    Lentopeli.delete()
else:
    player_info(id, fuel_budget, screen_name, fuel_left, yhteys)