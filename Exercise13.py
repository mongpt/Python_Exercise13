
from flask import Flask, Response
import json

#1
app = Flask(__name__)
@app.route('/prime_number/<num>')
def isPrime(num):
    result = True
    halfNum = round(int(num) / 2) + 1
    for i in range(2, halfNum):
        if int(num)%i==0:
            result = False
            break
    response = {
        "Number": int(num),
        "isPrime": result
    }
    json_data = json.dumps(response)
    http_response = Response(response=json_data, mimetype="application/json")
    return http_response

#2
import mysql.connector
myDb = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='root',
    autocommit=True
)

def getAirportInfo(icao):
    sql = "SELECT name,municipality FROM airport WHERE ident='" + icao + "';"
    myCursor = myDb.cursor()
    myCursor.execute(sql)
    query_result = myCursor.fetchall()
    if myCursor.rowcount > 0:
        for item in query_result:        # get only the first match
            return item[0], item[1]


@app.route('/airport/<icao>')      # decorator
def airport(icao):
    name, municipality = getAirportInfo(icao)
    response = {
        "ICAO": icao,
        "Name": name,
        "Location": municipality
    }

    json_data = json.dumps(response)
    http_response = Response(response=json_data, mimetype="application/json")
    return http_response

if __name__=='__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)