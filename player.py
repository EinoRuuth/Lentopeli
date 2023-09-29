import connector

yhteys = connector.sqlyhteys("admin")

id= 1 
fuel_budget = 1000
screen_name = "player"
fuel_left = 1000
treasures = 0

def delete():
    sql = "delete from players"
    kursori = yhteys.cursor()
    kursori.execute(sql)
    print(kursori.rowcount, "rows cleared.")
