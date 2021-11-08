from flask import Flask, jsonify
import urllib.request
import json

app = Flask(__name__)

@app.route("/<stop>", methods=['GET'])
def getArrivals(stop):
    with open('routesAtEachStop.json','r', encoding='utf-8') as f:
        routesAtEachStop = json.loads(f.read())

    with open('postedStopIDMapping.json', 'r', encoding='utf-8') as f:
        stopMap = json.loads(f.read())

    with open('rtaStops.geojson', 'r', encoding='utf-8') as f:
        rtaStops = json.loads(f.read())

    # First, we find the name of the transit stop using the sign's posted Stop #.
    try:
        rtaStopName = list(filter(lambda x:x["properties"]["stop_id"]==stop,rtaStops['features']))[0]['properties']['stop_name']
    except:
        return jsonify({"error": "Stop # not found.", "request": stop}), 400, {'ContentType':'application/json'}

    # Second, we find the internal NextConnect system's stopID, which is different than the sign's posted Stop #.
    stopID = str(stopMap[stop])

    # Third, we find all of the routes that visit the transit stop.
    routeID = routesAtEachStop[stopID]

    # Next, we query GCRTA's NextConnect API for arrivals at the transit stop for each transit route.
    urlNextConnect = 'http://nextconnect.riderta.com/Arrivals.aspx/getStopTimes'

    arrivals = []
    for route in routeID.split('_'):
        params = json.dumps({"routeID": route.split('-')[0], "directionID": route.split('-')[1], "stopID": stopID, "tpID": 0, "useArrivalTimes": "false"}).encode('utf8')
        req = urllib.request.Request(urlNextConnect, data=params,
                                     headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf8'))

        # Next, we merge all of the API response data into a single list.
        arrivals.append(data)

    # Finally, we return the requested arrival data using JSON, and return the 200 success code.
    return jsonify({"stopName": rtaStopName, "arrivals": arrivals, "request": stop}), 200, {'ContentType':'application/json'}
