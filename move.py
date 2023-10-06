import connector

yhteys = connector.sqlyhteys("menat44")


def hakija( yhteys):
    sql = "SELECT airport_name FROM game"
    # randomi order että ei ole aakkosjärjestys
    sql += " ORDER BY RAND ( )"
    # limitoi etsinnät 1
    sql += " LIMIT 1 "
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos[0][0]

def treasure_check(aarre, tavarat, yhteys):
    lentokentan_nimi = tavarat[0][0]
    aarteen_nimi = aarre[0][0]
    merkkijono = ""
    if aarre[0][0]:
        sql1 = "UPDATE players SET treasures='"+aarre[0][0]+"' WHERE id='"+"1"+"'"
        sql2 = "UPDATE game SET treasure='"+"(NULL)"+"' WHERE treasure='"+str(aarteen_nimi)+"'"
        kursori = yhteys.cursor()
        kursori.execute(sql1)
        kursori = yhteys.cursor()
        kursori.execute(sql2)
        merkkijono = (f"{lentokentan_nimi}ssä on aarre. Aarre lisätty ruumaan")
    else:
        merkkijono = (f"{lentokentan_nimi}ssä ei ole aarretta")
    return merkkijono


def treasure_haku(tavarat, yhteys):
    lentokentan_nimi = tavarat[0][0]
    sql = "SELECT treasure FROM game"
    sql += " WHERE (airport_name='"+lentokentan_nimi+"')"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    aarre = kursori.fetchall()
    print(treasure_check(aarre, lentokenttä, yhteys))
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
        treasure_haku(lentokenttä, yhteys)
        return True
    else:
        return False


lentokenttä = hakija(yhteys)
liikkuminen = move(lentokenttä, yhteys)
if not liikkuminen:
    exit("GAMER OVER!\nYou ran out of fuel.")