import random as rd
import connector

yhteys = connector.sqlyhteys("admin")

id= 1 
fuel_budget = 1000
screen_name = "player"
fuel_left = 1000
treasures = 0

def hae(players,yhteys):
    takenplayers = []
    for playername in players:
        sql = "INSERT INTO players (id, fuel_budget, fuel_left, treasures, location, screen_name) VALUES (%s)"
        val = (playername)
        kursori = yhteys.cursor()
        kursori.execute(sql, val)
    return
