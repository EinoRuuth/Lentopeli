import gamecreator
import move
import connector
import sys
import pikkufunktiot
from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()
sqlpass = os.getenv('sqlpass')
yhteys = connector.sqlyhteys(sqlpass)
kursori = yhteys.cursor()

clargs = (sys.argv)

# config starts
# tavaroitten määrät ja nimet
itemtons = ["8 tonnia", "10 tonnia", "11 tonnia", "12 tonnia",
            "14 tonnia", "16 tonnia", "18 tonnia", "19 tonnia",
            "20 tonnia", "23 tonnia"]
itemnames = ["aurinkopaneeleita", "puutavaraa", "teräslevyjä",
             "sähkölaitteita", "tekstiileitä", "säilykkeitä",
             "työkaluja", "postia", "rakennustarvikkeita",
             "koneiden varaosia"]

if len(clargs) > 0 and clargs[0] == "run":
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'


    @app.route('/creategame/<limit>/<distance>/<name>/<gamecountry>')
    def creategame(limit, distance, name, gamecountry):
        try:
            createdgame = gamecreator.gamemaker(kursori, gamecountry, int(limit), int(distance))
            gamecreator.player_info(kursori, createdgame[0]['name'], 1, 5, name)
        except Exception as e:
            print(e)
            return [{'code': 500, 'message': f'error "{e}" occurred when creating game'}]
        return [{'code': 200, 'message': 'game and player successfully created',
                 'data': {'gamedata': createdgame, 'playerdata': createdgame[0]}}]


    @app.route('/cleardata')
    def cleardata():
        try:
            pikkufunktiot.cleardatabase(kursori)
        except Exception as e:
            print(e)
            return [{'code': 500, 'message': f'error "{e}" occurred when clearing database'}]
        return [{'code': 200, 'message': 'database cleared successfully'}]


    @app.route('/playerdata')
    def playerdata():
        try:
            pdata = (pikkufunktiot.getplayerdata(kursori))
            fuel_left = pdata[2]
            treasures = pdata[3]
            location = pdata[4]
            pdatadict = {'fuel': fuel_left, 'treasures': treasures, 'location': location}
        except Exception as e:
            print(e)
            return [{'code': 500, 'message': f'error "{e}" occurred when fetching playerdata'}]
        return [{'code': 200, 'message': 'playerdata fetched successfully', 'data': pdatadict}]


    @app.route('/calculatefuel/<airport1>/<airport2>')
    def calculatefuel(airport1, airport2):
        try:
            fueldata = move.fuelcalc(kursori, airport1, airport2)
        except Exception as e:
            print(e)
            return [{'code': 500, 'message': f'error "{e}" occurred when calculating fuel'}]
        return [{'code': 200, 'message': 'fuel calculated successfully', 'data': fueldata}]


    @app.route('/move/<targetairport>/<fuelconsumption>')
    def move(targetairport, fuelconsumption):
        try:
            movedata = move.move(targetairport, fuelconsumption)
        except Exception as e:
            print(e)
            return [{'code': 500, 'message': f'error "{e}" occurred while trying to move'}]
        return [{'code': 200, 'data': movedata}]


    if __name__ == '__main__':
        app.run(use_reloader=True, host='127.0.0.1', port=3000)
else:
    if __name__ == '__main__':
        if len(clargs) > 0 and clargs[0] == "del":
            pikkufunktiot.cleardatabase(kursori)
        else:
            createdgame = gamecreator.gamemaker(kursori, 'FI', 20, 200)
            gamecreator.player_info(kursori, createdgame[0]['name'], 1, 5, 'bob')
