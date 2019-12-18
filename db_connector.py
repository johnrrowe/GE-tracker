import requests
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.constants import ClientFlag

config = {
  'host':'osrs.mysql.database.azure.com',
  'user':'jrrowe@osrs',
  'password':'Bigrig92',
  'database':'items'
}

def connect_to_db():
    # Construct connection string
    try:
       conn = mysql.connector.connect(**config, client_flags=[ClientFlag.LOCAL_FILES])
       print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
          print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
          print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

    return conn, cursor
