
import indeed, linkedin, simplyhired

bots = ['indeed','linkedin', 'simplyhired']

modules = map(__import__, bots)

import multiprocessing

multiprocessing.Process(target=modules)




# DATABASE CONNECTION

import pymysql

# Open database connection
db = pymysql.connect("localhost","root","root","jobs")
print ("\n\nConnecting database ...\n\n")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# drop table
try:
    cursor.execute('DROP TABLE jobs')
except:
    print("There is no main table in database.")


import csv

#create table
sql = """CREATE TABLE jobs (
   Title TEXT,
   Company TEXT,
   City TEXT,
   Country TEXT,
   Type TEXT,
   Summary TEXT,
   Email TEXT,
   Website TEXT,
   Source TEXT,
   PostedDate TEXT) CHARSET=utf8mb4 COLLATE=utf8mb4_bin"""

cursor.execute(sql)
print ('..............................................')
print (str(sql) +"\n\n" +"A new table is created.")
print ('..............................................')

print ("\n\n\n" +"Inserting values into the table ..." + "\n\n\n")

with open('jobs.csv', encoding="utf8", newline='') as csvfile:
    csv_data = csv.reader(csvfile)
    for row in csv_data:
        sql = "insert into jobs (Title,Company,City,Country,Type,Summary,Email,Website,Source,PostedDate)" \
              "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');"%(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
            print("Success")
        except:
            db.rollback()
            print("Failed")

# remove main.csv file
import os
#os.remove('jobs.csv')

print ('..............................................')

#print ("\n\n\n" +"Calling filter_jobs ...  Please wait ... " + "\n\n\n")
#cursor.callproc('filter_jobs', args=())
print ('..............................................')

# Commit to database, finalize the changes
db.commit()

print(cursor.execute("select * from jobs"))

# disconnect from server
db.close()
print ("DISCONNECTED FROM SERVER")
