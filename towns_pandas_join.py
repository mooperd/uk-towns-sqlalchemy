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
database_connection_string = "mysql+pymysql://admin:pfm5mY2HjEdRYFNz@database-2.cilkxsowjw2p.af-south-1.rds.amazonaws.com/towns?charset=utf8mb4"
database_connection = create_engine(database_connection_string)

town_query = """
    SELECT 	  
    town.id,
    town.name,
    town.nuts_region,
    town.county_id
    FROM town
"""

county_query = """
    SELECT 	  
    county.id,
    county.name AS county_name,
    county.nation_id 
    FROM county
"""

nation_query = """
    SELECT 	  
    nation.id,
    nation.name AS nation_name
    FROM nation
"""


town = pd.read_sql_query(town_query, database_connection).set_index("id")
county = pd.read_sql_query(county_query, database_connection).set_index("id")
nation = pd.read_sql_query(nation_query, database_connection).set_index("id")

output = town.merge(
  county,
  left_on='county_id',
  right_index=True,
  suffixes=('_town', '_county')
)

print(output)
output.to_csv("output.csv")