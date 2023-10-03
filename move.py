import connector

yhteys = connector.sqlyhteys("admin")

mycursor = mydb.cursor()
sql = "UPDATE players SET fuel_left = '' WHERE address = ''"
mycursor.execute(sql)
mydb.commit()
print(mycursor.rowcount, "record(s) affected")

if fuel_left == 0:
    exit
#move hommma tarvii:
# lokaation päivitys player tietokantaan
# polttoaineen chekki jos ei riitä niin peli loppuu ja päivitys player tietokantaan
# treasure chekki ja sen lisäys player hommaa, ja poistaa game taulusta
# homabase chekki jos on tavara niin polttoainetta ja jos on saanut kaikki tavarat niin voittaa (pitää laskua kuinka monta arretta on viety dificultia vastaan)
# 