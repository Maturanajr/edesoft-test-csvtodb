import sqlalchemy
import pandas as pd
import os
try:
    from dotenv import load_dotenv

    #loads enviroment variables for db
    load_dotenv()
except:
    pass
DBHOST=os.getenv('DBHOST')
DBNAME= os.getenv('DBNAME')
DBPASS= os.getenv('DBPASS')
DBPORT= os.getenv('DBPORT')	
DBTABLE= os.getenv('DBTABLE')	
DBUSER= os.getenv('DBUSER')

def send_to_database(df):
    try:
        #makes database connection
        database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
        format(DBUSER, DBPASS, DBHOST, DBNAME))
        #insert dataframe in database
        df.to_sql(con=database_connection, name=DBTABLE, if_exists='append',index= False)
        #close connection
        database_connection.dispose()
        return True
    except Exception as e:
        print("Database connection failed due to {}".format(e))   
        return False 
        