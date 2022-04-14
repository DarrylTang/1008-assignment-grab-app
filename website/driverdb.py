import sqlite3
from sqlite3 import Error
class Driver:
    def __init__(self, driverId, driverName, driverLocation, driverRatings, carBrand, carPlate):
        self.driverId = driverId
        self.driverName = driverName
        self.driverLocation = driverLocation
        self.driverRatings = driverRatings
        self.carBrand = carBrand
        self.carPlate = carPlate
class DriverDatabase:
    DRIVER_ID_COL = 0
    DRIVER_NAME_COL = 1
    DRIVER_LOC_COL = 2
    DRIVER_RATINGS_COL = 3
    CAR_BRAND_COL = 4
    CAR_PLATE_COL = 5
    
    listOfDrivers = []

    def __init__(self):
        try:
            # will create driver.db if it doesn't exist
            self.conn = sqlite3.connect("website/drivers.db", check_same_thread=False)
            self.cur = self.conn.cursor()
            self.createTable()
        except Error as e:
            print(e)

    def createTable(self):
        createStatement = """ CREATE TABLE IF NOT EXISTS driversTable (
                                            driverId integer PRIMARY KEY AUTOINCREMENT,
                                            driverName text,
                                            driverLocation integer,
                                            driverRatings integer,
                                            carBrand text,
                                            carPlate text
                                        ); """
        self.cur.execute(createStatement)
        self.conn.commit()

        #after creating table, try to read table and populate list of drivers
        self.readTable()

    def readTable(self):
        # check if there are any sample data in table
        self.cur.execute("SELECT * FROM driversTable")
        exist = self.cur.fetchone()

        #if not, insert sample data
        if exist is None:
            self.insertDriver(Driver(-1, "Matthew", 3, 5, "Honda", "S123456"))
            self.insertDriver(Driver(-1, "Aster", 5, 4, "BMW", "S817549"))
            self.insertDriver(Driver(-1, "Samantha", 15, 2, "Toyota", "S812704"))
            self.insertDriver(Driver(-1, "Alex", 50, 1, "Honda", "S123456"))
            self.insertDriver(Driver(-1, "John", 70, 2, "BMW", "S763890"))
            self.insertDriver(Driver(-1, "Sam", 182, 3, "Hyundai", "S456789"))
        #else, return data from database
        else:
            self.cur.execute("SELECT * FROM driversTable")
            rows = self.cur.fetchall()
            for row in rows:
                self.listOfDrivers.append(Driver(row[self.DRIVER_ID_COL], row[self.DRIVER_NAME_COL], row[self.DRIVER_LOC_COL], row[self.DRIVER_RATINGS_COL], row[self.CAR_BRAND_COL], row[self.CAR_PLATE_COL]))

    # inserting a single driver
    def insertDriver(self, driver):
        insertStatement = "INSERT INTO driversTable (driverName, driverLocation, driverRatings, carBrand, carPlate) VALUES ('" + str(driver.driverName) + "', '" + str(driver.driverLocation) + "', '" + str(driver.driverRatings) + "', '" + str(driver.carBrand) + "', '" + str(driver.carPlate) + "')"
        self.cur.execute(insertStatement)
        
        # driver obj pass by reference, update the actual id in database
        driver.driverId = self.cur.lastrowid
        self.listOfDrivers.append(driver)

        self.conn.commit()

    def updateDriverLocation(self, driverId, newDriverLocation):
        updateStatement = "UPDATE driversTable SET driverLocation = " + str(newDriverLocation) + " where driverId = " + str(driverId)

        for driver in self.listOfDrivers:
            if driverId == driver.driverId:
                driver.driverLocation = newDriverLocation

        self.cur.execute(updateStatement)
        self.conn.commit()