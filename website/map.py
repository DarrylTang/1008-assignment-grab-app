#The following are the imports we used throughout the project

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
from .quickSort import *

import sqlite3
from sqlite3 import Error
from time import time, sleep

# this defines the file as our blueprint
map = Blueprint('map', __name__)  # easier to name it the same as ur file

#This runs the oneMap Api to retrive addresses data
def OneMapAPI_data_retreive(address):
    req = requests.get('https://developers.onemap.sg/commonapi/search?searchVal='+address+'&returnGeom=Y&getAddrDetails=Y&pageNum=1')
    resultsdict = eval(req.text)   #Stores the extracted data in a tuple
    return resultsdict  #Returns the result

#Building the referencing dataset(excel) to build dataset
new_dict_data_all = ""  #Declaring a null variable first
datastore = {}  #Declaring an empty dictionary
nodesArray = getNodesArray()  #Calling our predefined nodes

#True if using speed, else if using distance then false
distanceGraph = Graph(nodesArray)
distanceGraph.linkAllNodes(False)

speedGraph = Graph(nodesArray)
speedGraph.linkAllNodes(True)

#initialize driver database
driverDatabase = DriverDatabase()

filename = 'dataset_of_postal'

if os.path.isfile('dataset_of_postal'):  #Checks if the file exist in the directory
    
    print ("File exist")
    infile = open(filename,'rb')
    new_dict_data_all = pickle.load(infile)   #Loads the files
    infile.close()
    
else:
    print ("File not exist") #If the file doesnt exist we need to create it

    df = pd.read_csv("hdb-property-information.csv")
    df['Address'] = df['blk_no'] + " " + df['street'] 
    addresslist = list(df['Address'])[:12472]   
    postal = []   
    
    for i in addresslist:         
        postal.append(OneMapAPI_data_retreive(i)) #We run the addresses through oneAPI to generate the data such as address, street name and postal code
    for k in range(len(addresslist)):
        datastore[k] = postal[k]
    outfile = open(filename,'wb')

    pickle.dump(datastore,outfile)
    outfile.close()

# This functions check if the userinput is valid and retrieve the lat and long base on either address, roadname or postal code
def Check_Valid_User_Input(User_Input):
    for i in range(len(new_dict_data_all)):
        if (bool(new_dict_data_all[i]['results']) == False or bool(new_dict_data_all[i]) == False):
            continue
        else:
            if User_Input in new_dict_data_all[i]['results'][0]['ADDRESS'] or User_Input in new_dict_data_all[i]['results'][0]['ROAD_NAME'] or User_Input in new_dict_data_all[i]['results'][0]['POSTAL']:
                return new_dict_data_all[i]['results'][0]['LATITUDE'], new_dict_data_all[i]['results'][0]['LONGITUDE']

# Compares the address and return the nearest node base on distance
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

# Compares the user's location and return the nearest driver base on distance
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

def getGrabsharePath_T(AC , CB , CD , BD):
    
    #comparing shortest time
    path1 = AC[1]/60 + CB[1] / 60 + BD[1] / 60
    path2 = AC[1] / 60 + CD[1] / 60 + BD[1] / 60

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
            
            source_location_x = nodesArray[A].latitude
            source_location_y = nodesArray[A].longitude

            end_location_x = nodesArray[B].latitude
            end_location_y = nodesArray[B].longitude
            
            driverDatabase.updateDriverLocation(driver.driverId, B)

            #We need our comparison for pathing here
            location_path = distanceGraph.dijkstraAlgoGetPath(A, B)[0]

            location_path_speed = speedGraph.dijkstraAlgoGetPath(A, B)[0]
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

        value_button = request.form.get('check')
        print(value_button)

        #Checks if the user has inputed a valid location else prompt again
        if (Check_Valid_User_Input(starting_location)== None or Check_Valid_User_Input(ending_location)== None or Check_Valid_User_Input(starting_location) == Check_Valid_User_Input(ending_location)):
            print("Either User_Location Not Found or Similar PICKUP and DROPOFF point Selected, Please enter again :)")
            return render_template("map_page_multi.html",  data=data)
        
        else:
            A = Return_User_to_Node_Matching(Check_Valid_User_Input(starting_location))
            B = Return_User_to_Node_Matching(Check_Valid_User_Input(ending_location))

            #driver pick up passenger at point A
            driver = getNearestDriver(A)
            print(driver.driverName)

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
            DB = distanceGraph.dijkstraAlgoGetPath(D , B)
            
            AC_s = speedGraph.dijkstraAlgoGetPath(A , C)
            CB_s = speedGraph.dijkstraAlgoGetPath(C , B)
            CD_s = speedGraph.dijkstraAlgoGetPath(C , D)
            BD_s = speedGraph.dijkstraAlgoGetPath(B , D)
            DB_s = speedGraph.dijkstraAlgoGetPath(D , B)
            
            
            data.update({
                        'startx': source_location_x, 'starty': source_location_y, 'endx': end_location_x, 'endy':end_location_y ,
                        'startx_2': additional_source_location_x, 'starty_2': additional_source_location_y , 'endx_2': additional_end_location_x, 'endy_2': additional_end_location_y , 
                    })
            
            
            
            
            print(additional_UserPickup_Check(A , B , C , D))
            
            #if false, don't pick up 2nd passenger
            #if true, pick up passenger
            if (additional_UserPickup_Check(A , B , C , D) == False):
                if (getGrabsharePath_D(AC , CB , CD , BD) == 1 and getGrabsharePath_T(AC_s , CB_s , CD_s , BD_s) == 1):
                    
                    #A -> C -> B -> D
                    loc1 = AC[0]
                    loc2 = CB[0]
                    loc3 = BD[0]

                    loc4 = AC_s[0]
                    loc5 = CB_s[0]
                    loc6 = BD_s[0]
                    
                    
                    driverDatabase.updateDriverLocation(driver.driverId, D)
                    
                    return render_template("map_page_multi.html", data=data, lineCoord1=loc1 , lineCoord2=loc2 , lineCoord3=loc3 , lineCoord4=loc4 , lineCoord5=loc5 , lineCoord6=loc6 , choice = value_button)
                
                elif (getGrabsharePath_D(AC , CB , CD , BD) == 1 and getGrabsharePath_T(AC_s , CB_s , CD_s , BD_s) == 2):
                    
                    #A -> C -> B -> D
                    loc1 = AC[0]
                    loc2 = CB[0]
                    loc3 = BD[0]

                    loc4 = AC_s[0]
                    loc5 = CD_s[0]
                    loc6 = DB_s[0]
                    
                    
                    driverDatabase.updateDriverLocation(driver.driverId, D)
                    
                    return render_template("map_page_multi.html", data=data, lineCoord1=loc1 , lineCoord2=loc2 , lineCoord3=loc3 , lineCoord4=loc4 , lineCoord5=loc5 , lineCoord6=loc6 , choice = value_button)
                
                elif (getGrabsharePath_D(AC , CB , CD , BD) == 2 and getGrabsharePath_T(AC_s , CB_s , CD_s , BD_s) == 1):
                    
                    #A -> C -> B -> D
                    loc1 = AC[0]
                    loc2 = CD[0]
                    loc3 = DB[0]

                    loc4 = AC_s[0]
                    loc5 = CB_s[0]
                    loc6 = BD_s[0]
                    
                    
                    
                    driverDatabase.updateDriverLocation(driver.driverId, D)
                    
                    return render_template("map_page_multi.html", data=data, lineCoord1=loc1 , lineCoord2=loc2 , lineCoord3=loc3 , lineCoord4=loc4 , lineCoord5=loc5 , lineCoord6=loc6 , choice = value_button)
                
                else:
                    loc1 = AC[0]
                    loc2 = CD[0]
                    loc3 = DB[0]
                    
                    loc4 = AC_s[0]
                    loc5 = CD_s[0]
                    loc6 = DB_s[0]
                    
                    #A -> C -> D -> B
                    driverDatabase.updateDriverLocation(driver.driverId, B)
                
                    return render_template("map_page_multi.html", data=data, lineCoord1=loc1 , lineCoord2=loc2 , lineCoord3=loc3 , lineCoord4=loc4 , lineCoord5=loc5 , lineCoord6=loc6 , choice = value_button)
            else:
                # A -> B path only
                driverDatabase.updateDriverLocation(driver.driverId, B)
            
            print("It has entered the false zone")
            return render_template("map_page_multi.html", data=data)

        # runs on default, GET
        # data here requires default values or it will crash
    return render_template("map_page_multi.html", data=data)
  
@map.route('/drivers_detail')
def driver_detail(): 
    return render_template("drivers_detail.html", drivers=driverDatabase.listOfDrivers)

@map.route('/drivers_detail_by_id')
def drivers_detail_by_id(): 
    sortedArray = driverDatabase.listOfDrivers

    #sort by driverId in ascending order
    #lambda returns true/false if one object's id is greater than the other
    quickSort(sortedArray, 0, len(sortedArray)-1, lambda x, y: x.driverId > y.driverId)
    
    return render_template("drivers_detail.html", drivers=sortedArray)

@map.route('/drivers_detail_by_ratings')
def drivers_detail_by_ratings(): 
    sortedArray = driverDatabase.listOfDrivers

    #sort by driverId in ascending order
    #lambda returns true/false if one object's ratings is greater than the other
    quickSort(sortedArray, 0, len(sortedArray)-1, lambda x, y: x.driverRatings > y.driverRatings)
    
    return render_template("drivers_detail.html", drivers=sortedArray)