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
        itemton = rd.randint(0,4)
        itemname = rd.randint(0,4)
        itemfullname = itemtons[itemton]+" "+itemnames[itemname]
        allitems.append(itemfullname)
    return (allitems, airports)

def sqlinsert(items, airports, yhteys):
    takenairports = []
    for airportname in airports:
        sql = "INSERT INTO game (airport_name, has_visited, homebase) VALUES (%s, %s, %s)"
        val = (airportname[0], 0, 0)
        kursori = yhteys.cursor()
        kursori.execute(sql, val)
    for itemname in items:
        itemairport = rd.randint(0,len(airports)-1)
        while itemairport in takenairports and itemairport<len(airports):
            itemairport=itemairport+1
        takenairports.append(itemairport)
        itemairport = airports[itemairport]
        for x in itemairport:
            itemairport=x
        sql = "UPDATE game SET treasure='"+itemname+"' WHERE airport_name='"+itemairport+"'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
    homebaseairport = rd.randint(0,len(airports)-1)
    while homebaseairport in takenairports and homebaseairport<len(airports):
            homebaseairport=homebaseairport+1
    homebase = airports[homebaseairport]
    sql = "UPDATE game SET homebase='"+"1"+"' WHERE airport_name='"+homebase[0]+"'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return