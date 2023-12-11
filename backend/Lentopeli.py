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
        pikkufunktiot.init(gamecountry)
        try:
            createdgame = gamecreator.gamemaker(kursori, gamecountry, int(limit), int(distance))
            gamecreator.player_info(kursori, createdgame[0]['name'], 1, 5, name)
            pikkufunktiot.init(gamecountry)
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


    @app.route('/drawtreasure/<wonminigame>/<chance>')
    def drawtreasure(wonminigame, chance):
        if wonminigame == 'True':
            try:
                treasure = pikkufunktiot.itemchance(chance, itemnames, kursori)
                try:
                    treasure['loss']
                    return [{'code': 200, 'message': 'treasure drawn successfully', 'data':treasure}]
                except:
                    fuelreachcheck = pikkufunktiot.checkfuel(kursori)
                    if fuelreachcheck:
                        return [{'code': 200, 'message': 'treasure drawn successfully', 'data':treasure}]
                    else:
                        return [{'code': 200, 'message': 'treasure drawn successfully', 'data':{'loss': 'true','data': 'polttoaine ei riitä liikkumiseen minnekkään'}}]
            except Exception as e:
                print(e)
                return [{'code': 500, 'message': f'error "{e}" occurred when drawing treasure'}]
        else:
            try:
                loss = pikkufunktiot.losecheck(kursori)
            except Exception as e:
                print(e)
                return [{'code': 500, 'message': f'error "{e}" occurred when changing fuel'}]
            if loss:
                lossdata = {
                    'loss': 'true',
                    'data': 'polttoaine loppui'
                }
            else:
                fuelreachcheck = pikkufunktiot.checkfuel(kursori)
                if fuelreachcheck:
                    lossdata = {
                    'loss': 'false',
                    }
                else:  
                    lossdata = {
                    'loss': 'true',
                    'data': 'polttoaine ei riitä liikkumiseen minnekkään'
                    }
            return [{'code': 200, 'message': 'fuel deducted successfully', 'data':lossdata}]


    @app.route('/playerdata')
    def playerdata():
        try:
            pdata, coords = (pikkufunktiot.getplayerdata(kursori))
            fuel_left = pdata[0]
            location = pdata[1]
            lon = coords[0]
            lat = coords[1]
            pdatadict = {'fuel': fuel_left, 'location': location, 'longitude': lon, 'latitude': lat}
        except Exception as e:
            print(e)
            return [{'code': 500, 'message': f'error "{e}" occurred when fetching playerdata'}]
        return [{'code': 200, 'message': 'playerdata fetched successfully', 'data': pdatadict}]


    @app.route('/calculatefuel/<airport1>/<airport2>')
    def calculatefuel(airport1, airport2):
        airport1 = airport1.replace("_", " ")
        airport2 = airport2.replace("_", " ")
        try:
            fueldata = move.fuelcalc(kursori, airport1, airport2)
        except Exception as e:
            print(e)
            return [{'code': 500, 'message': f'error "{e}" occurred when fetching calcfuel'}]
        return [{'code': 200, 'message': 'fuel calculated successfully', 'data': fueldata}]


    @app.route('/moveplayer/<targetairport>/<fuelconsumption>')
    def moveplayer(targetairport, fuelconsumption):
        targetairport = targetairport.replace("_", " ")
        try:
            movedata = move.move(kursori, targetairport, fuelconsumption)
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
            gamecountry = 'FI'
            pikkufunktiot.init(gamecountry)
            createdgame = gamecreator.gamemaker(kursori, gamecountry, 20, 200)
            gamecreator.player_info(kursori, createdgame[0]['name'], 1, 5, 'bob')
            