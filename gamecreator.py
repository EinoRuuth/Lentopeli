import random as rd

def hakija(limit, gamecountry, yhteys):
    sql = "SELECT name FROM airport"
    sql += " WHERE iso_country='"+gamecountry+"'"
    sql += " ORDER BY RAND ( )"
    sql += " LIMIT "+str(limit)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

def airports_items(items, airports, itemtons, itemnames, gamecountry, yhteys):
    airports = hakija(airports, gamecountry, yhteys)
    allitems = []
    for number in range(items):
        itemcolor = rd.randint(0,4)
        itemname = rd.randint(0,4)
        itemfullname = itemtons[itemcolor]+" "+itemnames[itemname]
        allitems.append(itemfullname)
    return (allitems, airports)

def sqlinsert(items, airports, yhteys):
    for airportname in airports:
        sql = "INSERT INTO game (airport_name) VALUES (%s)"
        val = (airportname)
        kursori = yhteys.cursor()
        kursori.execute(sql, val)
    for itemname in items:
        itemairport = rd.randint(0,len(airports)-1)
        itemairport = airports[itemairport]
        for x in itemairport:
            itemairport=x
        sql = "UPDATE game SET treasure='"+itemname+"' WHERE airport_name='"+itemairport+"'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
    return