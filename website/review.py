import sqlite3 as sql

conn = sql.connect('sortDriverRating.db')
c = conn.cursor()

allDrivers = [
    (1, 'Jacky', 'S123456', 'Honda', 119, 118, 5),
    (2, 'Kristin', 'S456789', 'BMW', 116, 171, 5),
    (3, 'Johnson', 'S987654', 'Toyota', 182, 181, 3),
    (4, 'Jessie', 'S763890', 'Hyundai', 130, 124, 4),
    (5, 'Daniel', 'S583918', 'Honda', 187, 188, 2),
    (6, 'Sammy', 'S923478', 'Hyundai', 183, 184, 5),
    (7, 'Mandy', 'S871347', 'Toyota', 166, 167, 2),
    (8, 'Kate', 'S962160', 'BMW', 139, 140, 5),
    (9, 'Yumi', 'S762937', 'Honda', 140, 141, 4),
    (10, 'Ben', 'S823471', 'Honda', 164, 165, 3),
    (11, 'Cassy', 'S817549', 'BMW', 143, 177, 3),
    (12, 'Leon', 'S965417', 'Toyota', 168, 111, 1),
    (13, 'Glenda', 'S871264', 'Hyundai', 112, 113, 5),
    (14, 'Jerry', 'S817492', 'BMW', 115, 114, 1),
    (15, 'Nancy', 'S812704', 'BMW', 109, 87, 5)
]


# createTable = """CREATE TABLE driversTable(
#     driverId integer,
#     driverName text,
#     carPlate text,
#     carType text,
#     driverLat text,
#     driverLong text,
#     driverRate integer
# )"""

# # CREATE TABLE
# c.execute(createTable)
# print("Created Database Table!")

# final
# https://pythonguides.com/python-sort-list-of-tuples/
def bubbleSortReview(arr):
    lastCol = len(arr)                          # get last column of allDrivers
    for j in range(0, lastCol):                 # loop through entire allDrivers tuple
        for i in range(0, lastCol - j - 1):     # compare each tuple pair of allDrivers
            if arr[i][-1] > arr[i + 1][-1]:     # arr[element][count], check key of the last element and compare
                temp = arr[i]
                arr[i] = arr[i + 1]
                arr[i + 1] = temp
    return arr                                  # return sorted tuples


bubbleSortReview(allDrivers)
# print('Sorted list:', allDrivers)

c.execute("SELECT * FROM driversTable")
rows = c.fetchall()
for row in rows:
    print(row)

# INSERT DATA

# insertDataSql = "INSERT INTO sortedDriverRatingTable VALUES (?, ?, ?, ?, ?, ?)"
# c.executemany(insertDataSql, allDrivers)
# print("Successfully added data!")

conn.commit()
conn.close()

# print(allDrivers)
