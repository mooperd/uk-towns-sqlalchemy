from sqlalchemy import create_engine
import pandas as pd

# Use 3 decimal places in output display
pd.set_option("display.precision", 3)
# Don't wrap repr(DataFrame) across additional lines
pd.set_option("display.expand_frame_repr", False)
# Set max rows displayed in output to 25
pd.set_option("display.max_rows", 25)

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = "localhost" 
database = 'towns' 
username = 'root' 
password = 'root'  

# database_connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
database_connection_string = "mysql+pymysql://admin:pfm5mY2HjEdRYFNz@database-2.cilkxsowjw2p.af-south-1.rds.amazonaws.com/towns"
database_connection = create_engine(database_connection_string)

query = """
    SELECT 	  
    journey.id,
    journey.from_town_id,
    journey.to_town_id,
    from_town.name AS from_town,
    to_town.name AS to_town
    FROM journey
    LEFT JOIN town from_town ON from_town.id = journey.from_town_id
    LEFT JOIN town to_town ON to_town.id = journey.to_town_id
    LIMIT 1000;





    /*         
            LEFT JOIN county from_county ON from_town.county_id = from_county.id
            LEFT JOIN county to_county ON to_town.county_id = to_county.id 
                to_town.name AS to_town,
    from_county.name AS from_county,
    to_county.name AS to_county
    WHERE (from_county.name = 'Herefordshire' AND to_county.name = 'Warwickshire')*/
"""


journey = pd.read_sql_query(query, database_connection).set_index("id")
print(journey)

