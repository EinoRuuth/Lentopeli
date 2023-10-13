def fullairportname(name, kursori):
    sql = "SELECT airport_name from game WHERE airport_name LIKE '" + name + "%'"
    kursori.execute(sql)
    fullairportname = kursori.fetchall()
    if len(fullairportname):
        airport = fullairportname[0][0]
    else:
        return False
    return airport


def cleardatabase(kursori):
    sql = "delete from game"
    kursori.execute(sql)
    sql = "delete from players"
    kursori.execute(sql)
    print("Tietokanta tyhjennetty")


def treasureamount(kursori):
    sql = "SELECT treasure FROM game"
    kursori.execute(sql)
    tulos = kursori.fetchall()
    luku = 0
    for x in tulos:
        if x[0] != "(NULL)" and x[0] != None:
            luku += 1
    return luku


def fuelamount(kursori):
    sql = "SELECT fuel_left FROM players"
    kursori.execute(sql)
    fuelleft = kursori.fetchall()[0][0]
    return fuelleft


def playerlocation(kursori):
    sql = "SELECT location FROM players"
    kursori.execute(sql)
    currentlocation = kursori.fetchall()[0][0]
    return currentlocation
