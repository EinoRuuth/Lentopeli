import random as rd
import connector

yhteys = connector.sqlyhteys("admin")

id= 1 
fuel_budget = 1000
screen_name = "player"
fuel_left = 1000
treasures = 0

def hae(items,players,yhteys):
    playerss = []
    for playername in players:
        sql = "INSERT INTO players (screen_name) VALUES (%s)"
        val = (playername)
        kursori = yhteys.cursor()
        kursori.execute(sql, val)
    for itemname in items:
        itemairport = rd.randint(0,len(players)-1)
        while itemairport in playerss and itemairport<len(players):
            itemairport=itemairport+1
        playerss.append(itemairport)
        itemairport = players[itemairport]
        for x in itemairport:
            itemairport=x
        sql = "UPDATE game SET treasure='"+itemname+"' WHERE airport_name='"+itemairport+"'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
    return
