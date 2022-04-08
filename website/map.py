from asyncio.windows_events import NULL
from lib2to3.pgen2 import driver
from flask import Blueprint, render_template, request
import pandas as pd
import requests
import sys

import haversine
import os
import pickle
from .nodes import *
import random
from .dijkstra import *
from .driverdb import *

import sqlite3
from sqlite3 import Error

from time import time, sleep

# this defines the file as our blueprint
map = Blueprint('map', __name__)  # easier to name it the same as ur file



#This runs the oneMap Api to retrive addresses data
def OneMapAPI_data_retreive(address):
    req = requests.get('https://developers.onemap.sg/commonapi/search?searchVal='+address+'&returnGeom=Y&getAddrDetails=Y&pageNum=1')
    resultsdict = eval(req.text)
    
    return resultsdict

#Building the referencing dataset(excel) to build dataset

new_dict_data_all = ""
datastore = {}
nodesArray = getNodesArray()

#True if using speed, else if using distance then false
distanceGraph = Graph(nodesArray)
distanceGraph.linkAllNodes(False)

speedGraph = Graph(nodesArray)
speedGraph.linkAllNodes(True)

#initialize driver database
driverDatabase = DriverDatabase()

filename = 'dataset_of_postal'

if os.path.isfile('dataset_of_postal'):
    print ("File exist")
    infile = open(filename,'rb')
    new_dict_data_all = pickle.load(infile)
    infile.close()
    
    
else:
    print ("File not exist")

    df = pd.read_csv("hdb-property-information.csv")
    df['Address'] = df['blk_no'] + " " + df['street']
    addresslist = list(df['Address'])[:12472]
    postal = []   
    for i in addresslist:
        postal.append(OneMapAPI_data_retreive(i))
    for k in range(len(addresslist)):
        datastore[k] = postal[k]
    outfile = open(filename,'wb')

    pickle.dump(datastore,outfile)
    outfile.close()


def Check_Valid_User_Input(User_Input):
    for i in range(len(new_dict_data_all)):
        if (bool(new_dict_data_all[i]['results']) == False or bool(new_dict_data_all[i]) == False):
            continue
        else:
            if User_Input in new_dict_data_all[i]['results'][0]['ADDRESS'] or User_Input in new_dict_data_all[i]['results'][0]['ROAD_NAME'] or User_Input in new_dict_data_all[i]['results'][0]['POSTAL']:
                return new_dict_data_all[i]['results'][0]['LATITUDE'], new_dict_data_all[i]['results'][0]['LONGITUDE']


def Return_User_to_Node_Matching(userinput):
    minimum_dist = minimum = sys.maxsize

    user_location = (float(userinput[0]) , float(userinput[1]))
        
    for i in range(0,len(nodesArray)):
        location = (nodesArray[i].latitude, nodesArray[i].longitude)
        
        distance = haversine(user_location, location, unit=Unit.METERS)

        if distance< minimum_dist:
            minimum_dist = distance
            minimum = i
            
    return minimum

def getNearestDriver(userNode):
    minimum_dist = sys.maxsize
    user_location = (nodesArray[userNode].latitude, nodesArray[userNode].longitude)

    #go through each driver in database
    for driver in driverDatabase.listOfDrivers:
        driver_location = (nodesArray[driver.driverLocation].latitude, nodesArray[driver.driverLocation].longitude)
        
        distance = haversine(user_location, driver_location, unit=Unit.METERS)

        if distance < minimum_dist:
            minimum_dist = distance
            driverAssigned = driver
            
    return driverAssigned


def additional_UserPickup_Check(A , B , C , D):
    
    
    AB = speedGraph.dijkstraAlgoGetPath(A , B)[1] / 60
    
    AC = speedGraph.dijkstraAlgoGetPath(A , C)[1] / 60
    
    CB = speedGraph.dijkstraAlgoGetPath(C , B)[1] / 60
    CD = speedGraph.dijkstraAlgoGetPath(C , D)[1] / 60
    
    BD = speedGraph.dijkstraAlgoGetPath(B , D)[1] / 60
        
    if ((AB * 2) > AC + CB + BD) or ((AB * 2) > AC + CD + BD):
        return True
    else:
        return False
    

def getGrabsharePath_D(AC , CB , CD , BD):
    #comparing shortest distance
    path1 = AC[1] + CB[1] + BD[1]
    path2 = AC[1] + CD[1] + BD[1]

    if (path1 <= path2):
        return 1 
    else:
        return 2

def getGrabsharePath_T(A , B , C , D):
    
    AC = speedGraph.dijkstraAlgoGetPath(A , C)[1] / 60
    
    CB = speedGraph.dijkstraAlgoGetPath(C , B)[1] / 60
    CD = speedGraph.dijkstraAlgoGetPath(C , D)[1] / 60
    
    BD = speedGraph.dijkstraAlgoGetPath(B , D)[1] / 60
        
    #comparing shortest time
    path1 = AC + CB + BD
    path2 = AC + CD + BD

    if (path1 <= path2):
        return 1 
    else:
        return 2



@map.route('/map_page', methods=['GET', 'POST'])  # add url here
def read_map():
    #To pass back into the html Side
    data = {'startx': 1.43589365, 'starty': 103.8007271}


    if request.method == 'POST':
        print("executing the POST....")

        #Process User INput
        starting_location = request.form.get('myLocation')
        ending_location = request.form.get('mydestination')


        #Clean up the userInput 
        starting_location = starting_location.strip('\r\n      ')
        ending_location = ending_location.strip('\r\n      ')


        starting_location= starting_location.upper()
        ending_location = ending_location.upper()


        #Print the user input into the terminal
        print(starting_location)
        print(ending_location)

        #Checks if the user has inputed a valid location else prompt again
        if (Check_Valid_User_Input(starting_location)== None or Check_Valid_User_Input(ending_location)== None or Check_Valid_User_Input(starting_location) == Check_Valid_User_Input(ending_location)):
            print("Either User_Location Not Found or Similar PICKUP and DROPOFF point Selected, Please enter again :)")
            return render_template("map_page.html", data=data)
        
        else:
            A = Return_User_to_Node_Matching(Check_Valid_User_Input(starting_location))
            B = Return_User_to_Node_Matching(Check_Valid_User_Input(ending_location))

            driver = getNearestDriver(A)
            print("MY NEAREST DRIVER IS: " + str(driver.driverName))
            
            source_location_x = nodesArray[A].latitude
            source_location_y = nodesArray[A].longitude

            print("updating driver loc to go to user loc to pickup")
            driverDatabase.updateDriverLocation(driver.driverId, A)

            end_location_x = nodesArray[B].latitude
            end_location_y = nodesArray[B].longitude
            
            print("updating driver loc to go to destination location to drop off")
            driverDatabase.updateDriverLocation(driver.driverId, B)

            #We need our comparison for pathing here
            location_path = distanceGraph.dijkstraAlgoGetPath(A, B)[0]
            
            #nodesNum = distanceGraph.dijkstraAlgoGetPath(A, B)[2]
            """print("DISTANCE PATH")
            print(location_path)
            print(nodesNum)
            """

            location_path_speed = speedGraph.dijkstraAlgoGetPath(A, B)[0]
            
            #nodesNo = speedGraph.dijkstraAlgoGetPath(A, B)[2]    
                   
            """print("SPEEDY PATH")
            print(location_path_speed)
            print(nodesNo)
            """
            data.update({
                'startx': source_location_x, 'starty': source_location_y, 'endx': end_location_x, 'endy':end_location_y
            })

            print(data)
            
            return render_template("map_page.html", data=data, lineCoord=location_path , lineCoord2=location_path_speed)
    return render_template("map_page.html", data=data)

    
    

# the grabshare portion
@map.route('/map_page_multi', methods=['GET', 'POST'])  # add url here
def read_map_multi():

    #To pass back into the html Side
    data = {'startx': 1.43589365, 'starty': 103.8007271}

    if request.method == 'POST':
        print("executing the POST....")

        print("executing the POST....")


        #Process User INput
        starting_location = request.form.get('myLocation')
        ending_location = request.form.get('mydestination')
        #Clean up the userInput 
        starting_location = starting_location.strip('\r\n      ')
        ending_location = ending_location.strip('\r\n      ')
        starting_location= starting_location.upper()
        ending_location = ending_location.upper()


        #Process User INput
        starting_location_2 = request.form.get('myLocation_2')
        ending_location_2 = request.form.get('mydestination_2')
        #Clean up the userInput 
        starting_location_2 = starting_location_2.strip('\r\n      ')
        ending_location_2 = ending_location_2.strip('\r\n      ')
        starting_location_2= starting_location_2.upper()
        ending_location_2 = ending_location_2.upper()


        #Checks if the user has inputed a valid location else prompt again
        if (Check_Valid_User_Input(starting_location)== None or Check_Valid_User_Input(ending_location)== None or Check_Valid_User_Input(starting_location) == Check_Valid_User_Input(ending_location)):
            print("Either User_Location Not Found or Similar PICKUP and DROPOFF point Selected, Please enter again :)")
            return render_template("map_page_multi.html",  data=data)
        
        else:
            A = Return_User_to_Node_Matching(Check_Valid_User_Input(starting_location))
            B = Return_User_to_Node_Matching(Check_Valid_User_Input(ending_location))



            source_location_x = nodesArray[A].latitude
            source_location_y = nodesArray[A].longitude
            
            
            end_location_x = nodesArray[B].latitude
            end_location_y = nodesArray[B].longitude
            
            
            C = Return_User_to_Node_Matching(Check_Valid_User_Input(starting_location_2))
            D = Return_User_to_Node_Matching(Check_Valid_User_Input(ending_location_2))
            
            additional_source_location_x = nodesArray[C].latitude
            additional_source_location_y = nodesArray[C].longitude
            
            additional_end_location_x = nodesArray[D].latitude
            additional_end_location_y = nodesArray[D].longitude
            
            #We need our comparison for pathing here
            
            AC = distanceGraph.dijkstraAlgoGetPath(A , C)
            CB = distanceGraph.dijkstraAlgoGetPath(C , B)
            CD = distanceGraph.dijkstraAlgoGetPath(C , D)
            BD = distanceGraph.dijkstraAlgoGetPath(B , D)
            
            
            
            #A TO B
            location_path = distanceGraph.dijkstraAlgoGetPath(A, B)[0]
            location_path_speed = speedGraph.dijkstraAlgoGetPath(A, B)[0]
            
            #C TO D
            additional_location_path = distanceGraph.dijkstraAlgoGetPath(C, D)[0]
            additional_location_path_speed = distanceGraph.dijkstraAlgoGetPath(C, D)[0]
            
            
            data.update({
                        'startx': source_location_x, 'starty': source_location_y, 'endx': end_location_x, 'endy':end_location_y ,
                        'startx_2': additional_source_location_x, 'starty_2': additional_source_location_y , 'endx_2': additional_end_location_x, 'endy_2': additional_end_location_y , 
                    })
            
            
            
            
            print(additional_UserPickup_Check(A , B , C , D))
            
            if (additional_UserPickup_Check(A , B , C , D) == False):
                
                
                if (getGrabsharePath_D(AC , CB , CD , BD) == 1):
                    
                    loc1 = AC[0]
                    loc2 = CB[0]
                    loc3 = BD[0]
                    
                    return render_template("map_page_multi.html", data=data, lineCoord1=loc1 , lineCoord2=loc2 , lineCoord3=loc3)
                else:
                    loc1 = AC[0]
                    loc2 = CD[0]
                    loc3 = BD[0]
                    
                
                    return render_template("map_page_multi.html", data=data, lineCoord1=loc1 , lineCoord2=loc2 , lineCoord3=loc3)
            
            
            
            
            print("It has entered the false zone")
            return render_template("map_page_multi.html", data=data)

        # runs on default, GET
        # data here requires default values or it will crash
    return render_template("map_page_multi.html", data=data)
  
    


       
