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
database_connection_string = 'mysql+pymysql://root:root@localhost/towns'
database_connection = create_engine(database_connection_string)

query = """
    SELECT 	  
    town.id,
    town.name,
    town.grid_reference,
    town.easting,
    town.northing,
    town.latitude,
    town.longitude,
    town.elevation,
    town.postcode_sector,
    town.local_government_area,
    town.nuts_region,
    town.town_type,
    FROM town
"""

df = pd.read_sql_query(query, database_connection)
print(df)


