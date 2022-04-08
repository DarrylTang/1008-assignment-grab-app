import requests

#onemap api gettoken
def getToken():
    tokenCredentials = {"email": "1008TestAcc@gmail.com", "password": "Me58Jx|';v~QCPa"}
    req = requests.post('https://developers.onemap.sg/privateapi/auth/post/getToken', data=tokenCredentials)
    resultsdict = eval(req.text)
    return resultsdict["access_token"]

#one map api auto routing
def getRoute(startGeo, endGeo):
    startGeo = startGeo[0] + "," + startGeo[1]
    endGeo = endGeo[0] + "," + endGeo[1]
    req = requests.get('https://developers.onemap.sg/privateapi/routingsvc/route?start=' + startGeo + '&end=' + endGeo + '&routeType=drive&token=' + getToken())
    resultsdict = eval(req.text)

    #returns encoded geometry route (from start to end)
    return resultsdict["route_geometry"]