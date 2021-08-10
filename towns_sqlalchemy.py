import csv # give python csv superpowers
import random
import geopy.distance
from model import dbconnect, Town, County, Nation, Journey

# SQL Errors
from sqlalchemy.orm.exc import NoResultFound

def addGetNation(session, nation_name_input):
    # Try and get the Nation from the database. If error (Except) add to the database.
    try:
        nation = session.query(Nation).filter(Nation.name == nation_name_input).one()
    except NoResultFound:
        nation = Nation()
        nation.name = nation_name_input
    return nation

def addGetCounty(session, county_name_input, nation_name_input):
    # Try and get the County from the database. If error (Except) add to the database.
    try:
        county = session.query(County).filter(County.name == county_name_input).one()
    except NoResultFound:
        county = County()
        county.nation = addGetNation(session, nation_name_input)
        county.name = county_name_input
    return county

def addTown(session, town_input):
    # Try and get the Country from the database. If error (Except) add to the database.
    town = Town()
    # Add attributes
    town.county = addGetCounty(session, town_input["county"], town_input["nation"])
    town.name = town_input["name"]
    town.grid_reference = town_input["grid_reference"]
    town.easting = town_input["easting"]
    town.northing = town_input["northing"]
    town.latitude = town_input["latitude"]
    town.longitude = town_input["longitude"]
    town.elevation = town_input["elevation"]
    town.postcode_sector = town_input["postcode_sector"]
    town.local_government_area = town_input["local_government_area"]
    town.nuts_region = town_input["nuts_region"]
    town.town_type = town_input["town_type"]
    # add the country (parent) to the county (child)
    session.add(town)
    session.commit()

def addJourney(session, towns):

    def getRandomTown(session, towns):
        row = int(len(towns)*random.random())
        return towns[row]
    
    def calculateDistance(town_pair):
        return geopy.distance.distance(
            (town_pair[0].latitude, town_pair[0].longitude),
            (town_pair[1].latitude, town_pair[1].longitude)).km

    # Try and get the Country from the database. If error (Except) add to the database.
    journey = Journey()
    journey.from_town = getRandomTown(session, towns)
    journey.to_town = getRandomTown(session, towns)
    journey.distance = calculateDistance([journey.from_town, journey.to_town])
    journey.number_of_passenges = 4
    journey.weight = 40
    journey.price = journey.distance * 1.1
    session.add(journey)
    

session = dbconnect()
"""
with open(r"uk-towns-sample.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for town in reader:
        addTown(session, town)

"""
towns = session.query(Town).all()
for i in range(100000):
    if i % 100 == 0:
        print('.', end='')
    addJourney(session, towns)
session.commit()


