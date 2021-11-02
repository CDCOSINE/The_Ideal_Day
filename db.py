import sqlite3
  
# connecting to the database
connection = sqlite3.connect("ideal_day_db.db")

crsr = connection.cursor()

sql_command = """CREATE TABLE records ( 
user_name INTEGER PRIMARY KEY, 
day VARCHAR(6),
tasks VARCHAR(100), 
score INTEGER);"""
  
# execute the statement
crsr.execute(sql_command)
  
# close the connection
connection.close()