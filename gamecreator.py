import random as rd


# hakija hakee sql tietokannasta annetun määrän (limit) lentokenttiä
def hakija(limit, gamecountry, yhteys):
    sql = "SELECT name FROM airport"
    sql += " WHERE (iso_country='"+gamecountry+"') AND (type='small_airport' OR type='medium_airport' OR type='large_airport')"
    # randomi order että ei ole aakkosjärjestys
    sql += " ORDER BY RAND ( )"
    # limitoi etsinnät 20
    sql += " LIMIT "+str(limit)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos


# arpoo itemit niiden määrän mukaan ja alussa callaa hakijaa
def airports_items(items, airports, itemtons,
                   itemnames, gamecountry, yhteys):
    airports = hakija(airports, gamecountry, yhteys)
    allitems = []
    for number in range(items):
        itemton = rd.randint(0, len(itemtons)-1)
        itemname = rd.randint(0, len(itemnames)-1)
        # ylhäällä arpoo numerot item listoista ja
        # alla se yhdistää ne ja lisää yhteyseen listaan
        itemfullname = itemtons[itemton]+" "+itemnames[itemname]
        allitems.append(itemfullname)
    return (allitems, airports)


# tämä lisää tavarat sql tietokantaan
def sqlinsert(items, airports, yhteys):
    takenairports = []
    airportid = 1
    for airportname in airports:
        # tämä täyttää nimen, has visited ja
        # homebase hommat nimillä ja nollilla
        sql = "INSERT INTO game (id, airport_name, has_visited, homebase) VALUES (%s, %s, %s, %s)"
        val = (airportid, airportname[0], 0, 0)
        kursori = yhteys.cursor()
        kursori.execute(sql, val)
        airportid += 1
    for itemname in items:
        # tämä arpoo tavaroiden kenttien numerot ja
        # tarkistaa että ei ole duplicateja
        itemairport = rd.randint(0, len(airports)-1)
        while itemairport in takenairports and itemairport < len(airports):
            itemairport = itemairport - 1
        takenairports.append(itemairport)
        itemairport = airports[itemairport]
        for x in itemairport:
            itemairport = x
        # tässä tavarat lisätään tietokantaan oikeisiin kohtiin
        sql = "UPDATE game SET treasure='" + itemname + "' WHERE airport_name='" + itemairport + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
    homebaseairport = rd.randint(0, len(airports)-1)
    # tämä arpoo homebasen samalla tavalla kun items ja
    # katsoo että homebasella ei ole tavaraa
    while homebaseairport in takenairports and homebaseairport < len(airports):
        homebaseairport = homebaseairport - 1
    homebase = airports[homebaseairport]
    # homebase lisätään tauluun joka laittaa sen kohdan byten 1
    sql = "UPDATE game SET homebase='"+"1"+"' WHERE airport_name='"+homebase[0]+"'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return


# Tämä funktio hakee game taulusta lentokentän jonka homebase arvo on 1
def homebase_haku(kursori):
    sql = "SELECT airport_name FROM game WHERE homebase=1"
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos[0][0]


# Tämä funktio lisää pelaajan players tietokantaan.
def player_info(id, fuel_budget, screen_name, fuel_left, yhteys):
    # Kutsutaan homebase_haku funktiota jotta saadaan
    # homebasen nimi tallenettia muuttujaan homebase
    kursori = yhteys.cursor()
    homebase = homebase_haku(kursori)
    # Lisätään pelaajan tiedot players tauluun
    sql = "INSERT INTO players (id, fuel_budget, Location, screen_name, fuel_left) VALUES (%s, %s, %s, %s, %s)"
    val = (id, fuel_budget, homebase, screen_name, fuel_left)
    kursori.execute(sql, val)
    return


def airportsearch(kursori):
    sql = "Select airport_name FROM game WHERE has_visited='0'"
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos
