<<<<<<< HEAD
<<<<<<< HEAD
import sqlite3
from sqlite3 import Error
class Driver:
    def __init__(self, driverId, driverName, driverLocation, carBrand, carPlate):
        self.driverId = driverId
        self.driverName = driverName
        self.driverLocation = driverLocation
        self.carBrand = carBrand
        self.carPlate = carPlate
class DriverDatabase:
    DRIVER_ID_COL = 0
    DRIVER_NAME_COL = 1
    DRIVER_LOC_COL = 2
    CAR_BRAND_COL = 3
    CAR_PLATE_COL = 4

    listOfDrivers = []

    def __init__(self):
        try:
            # will create driver.db if it doesn't exist
            self.conn = sqlite3.connect("website/drivers.db")
            self.cur = self.conn.cursor()
            self.createTable()
        except Error as e:
            print(e)

    def createTable(self):
        createStatement = """ CREATE TABLE IF NOT EXISTS driversTable (
                                            driverId integer PRIMARY KEY AUTOINCREMENT,
                                            driverName text,
                                            driverLocation integer,
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
            self.insertDriver(Driver(-1, "Matthew", 40, "Honda", "S123456"))
            self.insertDriver(Driver(-1, "Aster", 30, "BMW", "S817549"))
            self.insertDriver(Driver(-1, "Samantha", 15, "Toyota", "S812704"))
            self.insertDriver(Driver(-1, "Alex", 50, "Honda", "S123456"))
            self.insertDriver(Driver(-1, "John", 70, "BMW", "S763890"))
            self.insertDriver(Driver(-1, "Sam", 182, "Hyundai", "S456789"))
        #else, return data from database
        else:
            self.cur.execute("SELECT * FROM driversTable")
            rows = self.cur.fetchall()
            for row in rows:
                self.listOfDrivers.append(Driver(row[self.DRIVER_ID_COL], row[self.DRIVER_NAME_COL], row[self.DRIVER_LOC_COL], row[self.CAR_BRAND_COL], row[self.CAR_PLATE_COL]))

    # inserting a single driver
    def insertDriver(self, driver):
        insertStatement = "INSERT INTO driversTable (driverName, driverLocation, carBrand, carPlate) VALUES ('" + str(driver.driverName) + "', '" + str(driver.driverLocation) + "', '" + str(driver.carBrand) + "', '" + str(driver.carPlate) + "')"
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
=======
import sqlite3
from sqlite3 import Error
class Driver:
    def __init__(self, driverId, driverName, driverLocation, carBrand, carPlate):
        self.driverId = driverId
        self.driverName = driverName
        self.driverLocation = driverLocation
        self.carBrand = carBrand
        self.carPlate = carPlate
class DriverDatabase:
    DRIVER_ID_COL = 0
    DRIVER_NAME_COL = 1
    DRIVER_LOC_COL = 2
    CAR_BRAND = 3
    CAR_PLATE = 4

    listOfDrivers = []

    def __init__(self):
        try:
            # will create driver.db if it doesn't exist
            self.conn = sqlite3.connect("website/drivers.db")
            self.cur = self.conn.cursor()
            self.createTable()
        except Error as e:
            print(e)

    def createTable(self):
        createStatement = """ CREATE TABLE IF NOT EXISTS driversTable (
                                            driverId integer PRIMARY KEY AUTOINCREMENT,
                                            driverName text,
                                            driverLocation integer,
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
            self.insertDriver(Driver(-1, "Matthew", 40, "Honda", "S123456"))
            self.insertDriver(Driver(-1, "Aster", 30, "BMW", "S817549"))
            self.insertDriver(Driver(-1, "Samantha", 15, "Toyota", "S812704"))
            self.insertDriver(Driver(-1, "Alex", 50, "Honda", "S123456"))
            self.insertDriver(Driver(-1, "John", 70, "BMW", "S763890"))
            self.insertDriver(Driver(-1, "Sam", 182, "Hyundai", "S456789"))
        #else, return data from database
        else:
            self.cur.execute("SELECT * FROM driversTable")
            rows = self.cur.fetchall()
            for row in rows:
                self.listOfDrivers.append(Driver(row[self.DRIVER_ID_COL], row[self.DRIVER_NAME_COL], row[self.DRIVER_LOC_COL], row[self.CAR_BRAND], row[self.CAR_PLATE]))

    # inserting a single driver
    def insertDriver(self, driver):
        insertStatement = "INSERT INTO driversTable (driverName, driverLocation, carBrand, carPlate) VALUES ('" + str(driver.driverName) + "', '" + str(driver.driverLocation) + "', '" + str(driver.carBrand) + "', '" + str(driver.carPlate) + "')"
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
>>>>>>> parent of 34983c0 (update column naming)
        self.conn.commit()
=======
import sqlite3
from sqlite3 import Error


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
    


def main():
    database = r"drivers.db"

    # sql_create_driversTable = """ CREATE TABLE IF NOT EXISTS driversTable (
    #                                     driverId integer,
    #                                     driverName text,
    #                                     carPlate text,
    #                                     carType text,
    #                                     driverLat text,
    #                                     driverLong text,
    #                                     driverRate integer
    #                                 ); """

    # create a database connection
    conn = createConnection(database)
    # create tables
    # if conn is not None:
    #     # create projects table
    #     create_table(conn, sql_create_driversTable)

    #     # create tasks table
    #     # create_table(conn, sql_create_tasks_table)
    # else:
    #     print("Error! cannot create the database connection.")

    with conn:
        # create new driver data and insert
        # driver = (1, 'Jacky', 'S123456', 'Honda', 119, 118, 5);
        # driver = (2, 'Kristin', 'S456789', 'BMW', 116, 171, 5);
        # driver = (3, 'Johnson', 'S987654', 'Toyota', 182, 181, 3);
        # driver = (4, 'Jessie', 'S763890', 'Hyundai', 130, 124, 4);
        # driver = (5, 'Daniel', 'S583918', 'Honda', 187, 188, 2);
        # driver = (6, 'Sammy', 'S923478', 'Hyundai', 183, 184, 5);
        # driver = (7, 'Mandy', 'S871347', 'Toyota', 166, 167, 2);
        # driver = (8, 'Kate', 'S962160', 'BMW', 139, 140, 5);
        # driver = (9, 'Yumi', 'S762937', 'Honda', 140, 141, 4);
        # driver = (10, 'Ben', 'S823471', 'Honda', 164, 165, 3);
        # driver = (11, 'Cassy', 'S817549', 'BMW', 143, 177, 3);
        # driver = (12, 'Leon', 'S965417', 'Toyota', 168, 111, 1);
        # driver = (13, 'Glenda', 'S871264', 'Hyundai', 112, 113, 5);
        # driver = (14, 'Jerry', 'S817492', 'BMW', 115, 114, 1);
        # driver = (15, 'Nancy', 'S812704', 'BMW', 109, 87, 5);
        # createDrivers(conn, driver)

        # selectData(conn)

        i = 1
        while i < 6:
            updateDriver(conn, (70, 67, 1))
            selectUpdate(conn)
            i += 1
        # updateDriver(conn, (70, 67, 1))
        # selectUpdate(conn)
  

if __name__ == '__main__':
    main()


# old codes
# # https://www.youtube.com/watch?v=byHcYRpMgI4

# import sqlite3 as sql

# conn = sql.connect('drivers.db')
# c = conn.cursor()

# # SQL STATEMENTS

# # createTable = """CREATE TABLE driversTable(
# #     driverId integer,
# #     driverName text,
# #     carPlate text,
# #     carType text,
# #     driverLat text,
# #     driverLong text,
# #     driverRate integer
# # )"""

# # # CREATE TABLE
# # def createTable():
#     # c.execute(createTable)
#     # print("Created Database Table!")

# # insertDataSql = "INSERT INTO driversTable VALUES (?, ?, ?, ?, ?, ?, ?)"

# # INSERT DATA
# # allDrivers = [
# #     (1, 'Jacky', 'S123456', 'Honda', 119, 118, 5),
# #     (2, 'Kristin', 'S456789', 'BMW', 116, 171, 5),
# #     (3, 'Johnson', 'S987654', 'Toyota', 182, 181, 3),
# #     (4, 'Jessie', 'S763890', 'Hyundai', 130, 124, 4),
# #     (5, 'Daniel', 'S583918', 'Honda', 187, 188, 2),
# #     (6, 'Sammy', 'S923478', 'Hyundai', 183, 184, 5),
# #     (7, 'Mandy', 'S871347', 'Toyota', 166, 167, 2),
# #     (8, 'Kate', 'S962160', 'BMW', 139, 140, 5),
# #     (9, 'Yumi', 'S762937', 'Honda', 140, 141, 4),
# #     (10, 'Ben', 'S823471', 'Honda', 164, 165, 3),
# #     (11, 'Cassy', 'S817549', 'BMW', 143, 177, 3),
# #     (12, 'Leon', 'S965417', 'Toyota', 168, 111, 1),
# #     (13, 'Glenda', 'S871264', 'Hyundai', 112, 113, 5),
# #     (14, 'Jerry', 'S817492', 'BMW', 115, 114, 1),
# #     (15, 'Nancy', 'S812704', 'BMW', 109, 87, 5)
# # ]

# # c.executemany(insertDataSql, allDrivers)
# # print("Successfully added data!")

# # select drivers
# # def selectData():
# c.execute("SELECT * FROM driversTable")
# rows = c.fetchall()
# for row in rows:
#     print(row)
# # print("Selected all drivers")

#     # COMMIT AND CLOSE CONNECTION
# conn.commit()
# conn.close()

# # def main():
# #     conn = sql.connect('drivers.db')
# #     c = conn.cursor()
# #     with conn:
# #         selectData()

# # print(allDrivers)
>>>>>>> parent of da40c77 (update driver database to class database)
