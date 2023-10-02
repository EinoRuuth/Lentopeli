import random as rd
import connector

yhteys = connector.sqlyhteys("admin")

def hae(players,yhteys):
    takenplayers = []
    for playername in players:
        sql = "INSERT INTO players (id, fuel_budget, fuel_left, treasures, location, screen_name) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (playername[0], 0, 0)
        kursori = yhteys.cursor()
        kursori.execute(sql, val)
    return
