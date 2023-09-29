import random as rd

#hakija hakee sql tietokannasta annetun määrän (limit) lentokenttiä
def hakija(limit, gamecountry, yhteys):
    sql = "SELECT name FROM airport"
    sql += " WHERE iso_country='"+gamecountry+"'"
    #randomi order että ei ole aakkosjärjestys
    sql += " ORDER BY RAND ( )"
    #limitoi etsinnät 20
    sql += " LIMIT "+str(limit)
    kursori = yhteys.cursor()
    kursori.execute(sql)
    tulos = kursori.fetchall()
    return tulos

#arpoo itemit niiden määrän mukaan ja alussa callaa hakijaa
def airports_items(items, airports, itemtons, itemnames, gamecountry, yhteys):
    airports = hakija(airports, gamecountry, yhteys)
    allitems = []
    for number in range(items):
        itemton = rd.randint(0,len(itemtons)-1)
        itemname = rd.randint(0,len(itemnames)-1)
        #ylhäällä arpoo numerot item listoista ja alla se yhdistää ne ja lisää yhteyseen listaan
        itemfullname = itemtons[itemton]+" "+itemnames[itemname]
        allitems.append(itemfullname)
    return (allitems, airports)

#tämä lisää tavarat sql tietokantaan
def sqlinsert(items, airports, yhteys):
    takenairports = []
    for airportname in airports:
        #tämä täyttää nimen, has visited ja homebase hommat nimillä ja nollilla
        sql = "INSERT INTO game (airport_name, has_visited, homebase) VALUES (%s, %s, %s)"
        val = (airportname[0], 0, 0)
        kursori = yhteys.cursor()
        kursori.execute(sql, val)
    for itemname in items:
        #tämä arpoo tavaroiden kenttien numerot ja tarkistaa että ei ole duplicateja
        itemairport = rd.randint(0,len(airports)-1)
        while itemairport in takenairports and itemairport<len(airports):
            itemairport=itemairport+1
        takenairports.append(itemairport)
        itemairport = airports[itemairport]
        for x in itemairport:
            itemairport=x
        #tässä tavarat lisätään tietokantaan oikeisiin kohtiin
        sql = "UPDATE game SET treasure='"+itemname+"' WHERE airport_name='"+itemairport+"'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
    homebaseairport = rd.randint(0,len(airports)-1)
    #tämä arpoo homebasen samalla tavalla kun items ja katsoo että homebasella ei ole tavaraa
    while homebaseairport in takenairports and homebaseairport<len(airports):
            homebaseairport=homebaseairport+1
    homebase = airports[homebaseairport]
    #homebase lisätään tauluun joka laittaa sen kohdan byten 1
    sql = "UPDATE game SET homebase='"+"1"+"' WHERE airport_name='"+homebase[0]+"'"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    return