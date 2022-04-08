from asyncio.windows_events import NULL
from lib2to3.pgen2 import driver
from flask import Blueprint, render_template, request
import pandas as pd
import requests

import haversine
import os
import pickle
from .nodes import *
import random
from .dijkstra import *
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
from .driverDb import *
>>>>>>> parent of 2488034 (add nodes with edges file)
=======
>>>>>>> parent of da40c77 (update driver database to class database)
=======
>>>>>>> parent of da40c77 (update driver database to class database)

import sqlite3
from sqlite3 import Error

from time import time, sleep

# this defines the file as our blueprint
map = Blueprint('map', __name__)  # easier to name it the same as ur file

def getcoordinates(address):
    req = requests.get(
        'https://developers.onemap.sg/commonapi/search?searchVal=' + address + '&returnGeom=Y&getAddrDetails=Y&pageNum=1')
    resultsdict = eval(req.text)
    if len(resultsdict['results']) > 0:
        return resultsdict['results'][0]['LATITUDE'], resultsdict['results'][0]['LONGITUDE']
    else:
        pass

def getpostalcode(address):
    req = requests.get('https://developers.onemap.sg/commonapi/search?searchVal='+address+'&returnGeom=Y&getAddrDetails=Y&pageNum=1')
    resultsdict = eval(req.text)
    
    return resultsdict['results'][0]['POSTAL']

def findgeocoordinates(x):
    #search algos that can be used Boyer Moore , KMP , Finite Automata
    for i in datastore.keys():
        if (x == i):
            print(i)
            print("------------------------------------")
            print("Its a matchhhh")
            
            return getcoordinates(datastore[i])
        elif (x == datastore[i]):
            print(datastore[i])
            print("------------------------------------")
            print("Its a matchhhh")
            
            return getcoordinates(x)
        
        else:
            pass
                #print("Result not found")

def find_distance(userinput, nodesArray):
    minimum_dist = minimum = 728600
    
    print(userinput)
    for i in range(1,189):
        loc = (nodesArray[i].latitude, nodesArray[i].longitude)
        
        loc_user = (float(userinput[0]) , float(userinput[1]) )
        #distance = haversine(loc1, loc2)
        distance = haversine(loc_user, loc, unit=Unit.METERS)
        if distance< minimum_dist:
            minimum_dist = distance
            minimum = i
    
    return minimum

def ridesharePassenger_generator():
    return random.randint(1,180)

def ridesharePassenger_checker(passenger_pickup,passenger_dropoff,passenger_pickup_new,passenger_dropoff_new, nodesArray):
    Did_it_pass = False
    
    point_A = (nodesArray[passenger_pickup].latitude, nodesArray[passenger_pickup].longitude)
    point_B = (nodesArray[passenger_dropoff].latitude, nodesArray[passenger_dropoff].longitude)
    
    point_C = (nodesArray[passenger_pickup_new].latitude, nodesArray[passenger_pickup_new].longitude)
    point_D = (nodesArray[passenger_dropoff_new].latitude, nodesArray[passenger_dropoff_new].longitude)
    
    #Checker for A to C more than 30mins
    TIME_distance_A_C = haversine(point_A, point_C, unit=Unit.METERS) / 75
    print("The time taken from A to C is " + str(TIME_distance_A_C))
    #Checker for A to C more than 30mins
    TIME_distance_C_D = haversine(point_C, point_D, unit=Unit.METERS) / 75
    print("The time taken from C to D is " + str(TIME_distance_C_D))   
     
    if (TIME_distance_A_C > 30 or TIME_distance_C_D > 30):
        Did_it_pass = False
    else:
        Did_it_pass = True
    
    return Did_it_pass
    
def rideshareDistance_checker(passenger_pickup,passenger_dropoff,passenger_pickup_new,passenger_dropoff_new, nodesArray):
    point_A = (nodesArray[passenger_pickup].latitude, nodesArray[passenger_pickup].longitude)
    point_B = (nodesArray[passenger_dropoff].latitude, nodesArray[passenger_dropoff].longitude)
    
    point_C = (nodesArray[passenger_pickup_new].latitude, nodesArray[passenger_pickup_new].longitude)
    point_D = (nodesArray[passenger_dropoff_new].latitude, nodesArray[passenger_dropoff_new].longitude)
    
    #Checker for A to C to B to D
    distance_A_C_B_D = haversine(point_A, point_C, unit=Unit.METERS) + haversine(point_C, point_B, unit=Unit.METERS) + haversine(point_B, point_D, unit=Unit.METERS)
    
    #Checker for A to C to D to B
    distance_A_C_D_B = haversine(point_A, point_C, unit=Unit.METERS) + haversine(point_C, point_D, unit=Unit.METERS) + + haversine(point_D, point_B, unit=Unit.METERS)

    if (distance_A_C_B_D/75 > distance_A_C_D_B/75):
        return 2
    elif (distance_A_C_B_D/75 < distance_A_C_D_B/75):
        return 1
    elif (distance_A_C_B_D/75 == distance_A_C_D_B/75):
        return 1


#database stuff
def createConnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def createTable(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def createDrivers(conn, driversTable):
    sql = ''' INSERT INTO driversTable(driverId, driverName, carPlate, carType, driverLat, driverLong, driverRate)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, driversTable)
    conn.commit()
    return cur.lastrowid

def updateDriver(conn, driversTable):
    sql = ''' UPDATE driversTable
              SET driverLat = ? ,
                  driverLong = ?
              WHERE driverId = ?'''
    cur = conn.cursor()
    cur.execute(sql, driversTable)
    conn.commit()

def selectData(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM driversTable")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def selectUpdate(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM driversTable WHERE driverId = 1")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def drivers():
    conn = createConnection(database)
    with conn:
        i = random.randint(1,180)
        updateDriver(conn, (nodesArray[i].latitude, nodesArray[i].longitude, 1))
        selectUpdate(conn)
        
#Building the referencing dataset
filename = 'dataset_of_addresses'
datastore = {}
nodesArray = getNodesArray()
<<<<<<< HEAD
<<<<<<< HEAD
#True if using speed, else if using distance then false
distanceGraph = Graph(nodesArray)
distanceGraph.linkAllNodes(False)

speedGraph = Graph(nodesArray)
speedGraph.linkAllNodes(True)

if os.path.isfile('dataset_of_addresses'):
=======
=======
>>>>>>> parent of da40c77 (update driver database to class database)

filename = 'dataset_of_postal'

if os.path.isfile('dataset_of_postal'):
>>>>>>> parent of da40c77 (update driver database to class database)
    print ("File exist")
    infile = open(filename,'rb')
    datastore = pickle.load(infile)
    infile.close()
    print(datastore)
else:
    print ("File not exist")
        
    #get the excel
    df = pd.read_csv("website\static\hdb-property-information.csv")
            
    #fetch and format data from excel
    df['Address'] = df['blk_no'] + " " + df['street']
        #actual data is 12472 rows but for testing use 50
    addresslist = list(df['Address'])[:6000]
    datastore = {}
    for i in addresslist:
        datastore[getpostalcode(i)] = i
    
    outfile = open(filename,'wb')

    pickle.dump(datastore,outfile)
    outfile.close()

database = r"drivers.db"

# instead of using folium which limits a lot of functionality and documentation sucks, the variables and arrays here will be sent to a javascript file to make 
# use of leaflet
@map.route('/map_page', methods=['GET', 'POST'])  # add url here
def read_map():
    
    coor = ""
    coor_2 = ""
    
    data = {} # dictionary

    if request.method == 'POST':
        print("executing the POST....")
<<<<<<< HEAD
        
        # below is what is being typed in from the user.
=======



        #Process User INput
>>>>>>> parent of da40c77 (update driver database to class database)
        starting_location = request.form.get('myLocation')
        ending_location = request.form.get('mydestination')

        starting_location = starting_location.strip('\r\n      ')
        ending_location = ending_location.strip('\r\n      ')
        starting_location= starting_location.upper()
        ending_location = ending_location.upper()

        # perform check to prevent code from crashing
        if starting_location == "" or starting_location == "":
            print('input is empty')

        else:
            coor = findgeocoordinates(starting_location)
            coor_2 = findgeocoordinates(ending_location)

            print("Closest index for your starting location is " + str(find_distance(coor,nodesArray)))

            print("Closest index for your ending location is " + str(find_distance(coor_2,nodesArray)))
            sourceNode = find_distance(coor,nodesArray)
            destinationNode = find_distance(coor_2,nodesArray)

            #load the driver
            drivers()

            #pass reference of first node in the list to the graph class
            graph = Graph(nodesArray)
            graph.linkAllNodes()

            sl_x = nodesArray[sourceNode].latitude
            sl_y = nodesArray[sourceNode].longitude
            el_x = nodesArray[destinationNode].latitude
            el_y = nodesArray[destinationNode].longitude


            #loc is a 2D array of longitude and latitudes for pathing
            #format: loc = [[sl_x, sl_y], [el_x, el_y]]
            loc = distanceGraph.dijkstraAlgoGetPath(sourceNode, destinationNode)[0]
            print(loc)

            # taking the geo points on produced and sending it to the map in map_page
            data.update(
                {
                'startx': sl_x, 'starty': sl_y, 'endx': el_x, 'endy': el_y
                }
            )

            # print(data)

            return render_template("map_page.html", data=data, lineCoord=loc)

        #runs on default, GET
        # data here requires default values or it will crash
    return render_template("map_page.html", data=data)

# the grabshare portion
@map.route('/map_page_multi', methods=['GET', 'POST'])  # add url here
def read_map_multi():

<<<<<<< HEAD
<<<<<<< HEAD
    coor = ""
    coor_2 = ""
=======
=======
>>>>>>> parent of da40c77 (update driver database to class database)
    #True if using speed, else if using distance then false
    distanceGraph = Graph(nodesArray)
    distanceGraph.linkAllNodes(False)

    speedGraph = Graph(nodesArray)
    speedGraph.linkAllNodes(True)
    
    
    #To pass back into the html Side
    data = {'startx': 1.43589365, 'starty': 103.8007271}
>>>>>>> parent of da40c77 (update driver database to class database)

    data = {}  # dictionary

    if request.method == 'POST':
        print("executing the POST....")

        # below is what is being typed in from the user.
        starting_location = request.form.get('myLocation')
        ending_location = request.form.get('mydestination')

        starting_location = starting_location.strip('\r\n      ')
        ending_location = ending_location.strip('\r\n      ')
        starting_location = starting_location.upper()
        ending_location = ending_location.upper()

        # perform check to prevent code from crashing
        if starting_location == "" or starting_location == "":
            print('input is empty')

        else:
            #load the driver
            drivers()

            coor = findgeocoordinates(starting_location)
            coor_2 = findgeocoordinates(ending_location)

            print("Closest index for your starting location is " + str(find_distance(coor,nodesArray)))

            print("Closest index for your ending location is " + str(find_distance(coor_2,nodesArray)))
            sourceNode = find_distance(coor,nodesArray)
            destinationNode = find_distance(coor_2,nodesArray)
            
            sl_x = nodesArray[sourceNode].latitude
            sl_y = nodesArray[sourceNode].longitude

            el_x = nodesArray[destinationNode].latitude
            el_y = nodesArray[destinationNode].longitude

            #Rideshare function
            passenger_new_pickup  = ridesharePassenger_generator()
            passenger_new_dropoff = ridesharePassenger_generator()
            
            check = ridesharePassenger_checker(sourceNode,destinationNode,passenger_new_pickup,passenger_new_dropoff, nodesArray)
            
            print(check)
            
            if (check == True):
                passenger_new_pickup_x = nodesArray[passenger_new_pickup].latitude
                passenger_new_pickup_y = nodesArray[passenger_new_pickup].longitude
                
                passenger_new_dropoff_x = nodesArray[passenger_new_dropoff].latitude
                passenger_new_dropoff_y = nodesArray[passenger_new_dropoff].longitude
                
                #loc is a 2D array of longitude and latitudes for pathing
                #format: loc = [[sl_x, sl_y], [el_x, el_y]]
                
                loc = distanceGraph.dijkstraAlgoGetPath(sourceNode, destinationNode)[0]
                print(loc)
                
                path_picked = rideshareDistance_checker(sourceNode,destinationNode,passenger_new_pickup,passenger_new_dropoff, nodesArray)
                
                print(path_picked)
                
                if path_picked == 1:
                    path_A_C = distanceGraph.dijkstraAlgoGetPath(sourceNode,passenger_new_pickup)[0]
                    path_C_B = distanceGraph.dijkstraAlgoGetPath(passenger_new_pickup,destinationNode)[0]
                    path_B_D = distanceGraph.dijkstraAlgoGetPath(destinationNode,passenger_new_dropoff)[0]

                    # taking the geo points on produced and sending it to the map in map_page
                    data.update(
                        {
                        'startx': sl_x, 'starty': sl_y, 'endx': el_x, 'endy': el_y,
                        'startx_new': passenger_new_pickup_x, 'starty_new': passenger_new_pickup_y, 'endx_new': passenger_new_dropoff_x, 'endy_new': passenger_new_dropoff_y,
                        'choice': 1
                        }
                        )

                    print(data)
                    return render_template("map_page_multi.html", data=data, lineCoord_1=path_A_C , lineCoord_2=path_C_B , lineCoord_3=path_B_D)

                elif path_picked == 2:
                    path_A_C = distanceGraph.dijkstraAlgoGetPath(sourceNode,passenger_new_pickup)[0]
                    path_C_D = distanceGraph.dijkstraAlgoGetPath(passenger_new_pickup,passenger_new_dropoff)[0]
                    path_D_B = distanceGraph.dijkstraAlgoGetPath(passenger_new_dropoff,destinationNode)[0]
            
                    new_loc = path_A_C + path_C_D + path_D_B
                    
                    # taking the geo points on produced and sending it to the map in map_page
                    data.update(
                        {
                        'startx': sl_x, 'starty': sl_y, 'endx': el_x, 'endy': el_y,
                        'startx_new': passenger_new_pickup_x, 'starty_new': passenger_new_pickup_y, 'endx_new': passenger_new_dropoff_x, 'endy_new': passenger_new_dropoff_y,
                        'choice': 2
                        }
                        )

                    print(data)
                    
                    return render_template("map_page_multi.html", data=data, lineCoord_1=path_A_C , lineCoord_2=path_C_D , lineCoord_3=path_D_B)

        # runs on default, GET
        # data here requires default values or it will crash
        
        
    return render_template("map_page_multi.html", data=data)
  
    


       
