import sqlite3
from sqlite3 import Error
# from .DijkstraAlgo import *
from Nodes import *
import haversine as hs
# from website.DijkstraAlgo import *
# from Nodes import *
# from website import DijkstraAlgo
# # from .driverDb import *
# from .DijkstraAlgo import *

def createConnection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

def selectData(conn):
    cur = conn.cursor()
    # cur.execute("SELECT driverNode FROM driversTable")
    cur.execute("SELECT driverNode FROM driversTable WHERE driverId = 1")

    rows = cur.fetchall()

    for row in rows:
        # print(row)
        # print(row[0])
        return row[0]

# https://github.com/ashutoshb418/Foodies-Visualization/blob/master/Foodies_Chain.ipynb
# def distance_from(loc1,loc2): 
#     dist=hs.haversine(loc1,loc2)
#     return round(dist,2)
# nodesArray = getNodesArray()
# def distance_from(loc1,loc2): 
#     dist=hs.haversine(loc1,loc2)
#     return round(dist,2)

def distance_from(loc1,loc2): 
    dist=hs.haversine(loc1,loc2)
    return round(dist,2)

class Matching:
    def __init__(self):
        self.distanceToPassenger = []
    # def matchDriverToPassenger():

    def main():  
        database = r"C:\Users\cxuel\Documents\GitHub\1008-assignment-grab-app\website\drivers.db"
        conn = createConnection(database)
        passenger = 88
        passengerTest = 1.4354, 103.8029

        with conn:
            driver = selectData(conn)
            print(driver)
            driverTest = 1.4356, 103.8009
            distance_from(driverTest, passengerTest)
            # nodesDistance(driver, passenger)
            # test = nodesDistance(driver, passenger, getNodesArray())
            print("yay")
        


    if __name__ == '__main__':
        main()