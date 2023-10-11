import pikkufunktiot
import time


def treasure_check(aarre, tavarat, yhteys):
    lentokentan_nimi = tavarat
    aarteen_nimi = aarre[0][0]
    merkkijono = ""
    if aarteen_nimi:
        sql1 = "UPDATE players SET treasures='"+aarteen_nimi+"' WHERE id='"+"1"+"'"
        sql2 = "UPDATE game SET treasure='"+"(NULL)"+"' WHERE treasure='"+str(aarteen_nimi)+"'"
        kursori = yhteys.cursor()
        kursori.execute(sql1)
        kursori = yhteys.cursor()
        kursori.execute(sql2)
        merkkijono = (f"{lentokentan_nimi}ssä on rahtia. {aarteen_nimi} lisätty ruumaan")
        time.sleep(0.5)
    else:
        merkkijono = (f"{lentokentan_nimi}ssä ei ole rahtia")
    return merkkijono


def gotalltreasure(kursori):
    sql = "SELECT treasure FROM game"
    kursori.execute(sql)
    tulos = kursori.fetchall()
    luku = 0
    for x in tulos:
        if x[0] != "(NULL)" and x[0] != None:
            luku += 1
    if luku == 0:
        return True
    else:
        return False


def treasure_haku(tavarat, yhteys):
    lentokentan_nimi = tavarat
    sql = "SELECT treasure FROM game"
    sql += " WHERE (airport_name='"+lentokentan_nimi+"')"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    aarre = kursori.fetchall()
    if len(aarre) != 0:
        print(treasure_check(aarre, lentokentan_nimi, yhteys))
    else:
        print("ei löytynyt aarteita")
    return


def move(airport, yhteys):
    sql = "SELECT fuel_left FROM players"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    fuel= kursori.fetchall()
    fuel = fuel[0][0]
    if fuel >= 100:
        fuelleft = fuel-100
        sql1 = "UPDATE players SET location='" + airport + "'"
        sql2 = "UPDATE players SET fuel_left='" + str(fuelleft) + "'"
        sql3 = "UPDATE game SET has_visited=%s WHERE airport_name='"+ airport + "'"
        val3 = (1,)
        kursori.execute(sql1)
        kursori.execute(sql2)
        kursori.execute(sql3,val3)
        print(f"olet liikkunut {airport}ille")
        if homebasecheck(airport, yhteys):
            return
        treasure_haku(airport, yhteys)
        return
    else:
        pikkufunktiot.cleardatabase(kursori)
        exit("GAMER OVER!\nYou ran out of fuel.")
        return


def homebasecheck(airport, yhteys):
    sql = "SELECT airport_name FROM game WHERE homebase='1'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    homebase = kursori.fetchall()[0][0]
    if airport == homebase:
        print("olet nyt homebasessa")
        sql1 = "SELECT treasures FROM players"
        kursori.execute(sql1)
        treasure = kursori.fetchall()[0][0]
        if treasure.split(" ")[0] == "kultaisia":
            pikkufunktiot.cleardatabase(kursori)
            exit("VOITIT PELIN! Löysit harvinaisen rahdin")
        if treasure != "":
            print("sinulla on aarre, polttoaine täytetty")
            sql2 = "UPDATE players SET treasures = ''"
            kursori.execute(sql2)
            sql3 = "UPDATE players SET fuel_left= 1000"
            kursori.execute(sql3)
            if gotalltreasure(kursori):
                pikkufunktiot.cleardatabase(kursori)
                exit("VOITIT PELIN! Löysit kaikki rahdit")
        return True
    else:
        return False