import random as rd
from geopy import distance

def init(data):
    if data == "FI":
        diff = 5
    elif data == "US":
        diff = 10
    global difficulty
    difficulty = [diff]
    return difficulty

def cleardatabase(kursori):
    sql = "delete from game"
    kursori.execute(sql)
    sql = "delete from players"
    kursori.execute(sql)
    print("Tietokanta tyhjennetty")

def wincheck(kursori):
    sql = "SELECT treasures FROM players WHERE id='1'"
    kursori.execute(sql)
    playerdata = kursori.fetchall()[0][0]
    if playerdata is None:
        playerdata = 0
    if playerdata+1 == difficulty[0]:
        reason = f'Löysit {difficulty[0]} rahtia'
        return True, reason
    sql = f"UPDATE players SET treasures='{playerdata+1}' WHERE id='1'"
    kursori.execute(sql)
    return False, None

def losecheck(kursori):
    sql = "SELECT fuel_left FROM players WHERE id='1'"
    kursori.execute(sql)
    playerdata = kursori.fetchall()[0][0]
    if playerdata == 0:
        losedata = True
    else:
        losedata = False
    return losedata


def refuel(kursori):
    sql = "UPDATE players SET fuel_left='5' WHERE id='1'"
    kursori.execute(sql)

# Funktio ottaa prosentin ja laskee mahdollisuuden että löytyykö itemi vai ei.
# Jos itemi löytyy, lasketaan myös löytyykö harvinainen itemi vai ei.

def itemchance(percentage, itemnames, kursori):
    rareitempercentage = 1
    itemname = None
    found = False
    loss = False
    won = False
    winmessage = ''
    if rd.randint(0, 100) < int(percentage):
        found = True
        refuel(kursori)
        if rd.randint(0, 100) < rareitempercentage:
            itemname = f"golden {rd.choice(itemnames)}"
            won = True
            winmessage = 'Löysit harvinaisen rahdin'
        else:
            itemname = f"{rd.choice(itemnames)}"
            won, winmessage = wincheck(kursori)
    else:
        loss = losecheck(kursori)
    if loss:
        response = {
            'loss': 'lost',
            'data': 'polttoaine loppui'
        }
    else:
        response = {
            'found': found,
            'item': itemname,
            'won':won,
            'winmessage': winmessage
        }
    return response

def getplayerdata(kursori):
    sql = "SELECT fuel_left, location FROM players WHERE id='1'"
    kursori.execute(sql)
    playerdata = kursori.fetchall()[0]
    return playerdata

def checkfuel(kursori, location):
    sql = "SELECT fuel_left FROM players WHERE id='1'"
    kursori.execute(sql)
    fueldata = kursori.fetchall()[0][0]
    sql = f"SELECT airport_name, coordinates FROM game"
    kursori.execute(sql)
    coords2 = kursori.fetchall()
    location = location['data']
    coords1 = (location['latitude'], location['longitude'])
    for port in coords2:
        pituus = distance.distance(coords1, port[1:]).km
        pituus = round(pituus, 1)
        fuel = int((pituus // 50) + 1)
        if fuel <= fueldata:
            return True
    return False