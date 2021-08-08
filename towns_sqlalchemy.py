import csv # give python csv superpowers


from sqlalchemy import Integer, Column, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Errors
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()

# Country is currently the "parent" of everything. It is the "root".
class Nation(Base):
    __tablename__ = 'nation'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

class County(Base):
    __tablename__ = 'county'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    # We define the relationship between Country and County here.
    nation = relation("Nation", backref="county")
    nation_id = Column(Integer, ForeignKey('nation.id'))


# County is a child of Country
class Town(Base):
    __tablename__ = 'town'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    grid_reference = Column(String(64))
    easting = Column(Integer)
    northing = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Integer)
    postcode_sector = Column(String(64))
    local_government_area = Column(String(64))
    nuts_region = Column(String(64))
    town_type = Column(String(64))
    # We define the relationship between Country and County here.
    county = relation("County", backref="town")
    county_id = Column(Integer, ForeignKey('county.id'))


# A bunch of stuff to make the connection to the database work.
def dbconnect():
    engine = create_engine("mysql+pymysql://root:root@localhost/towns?charset=utf8mb4")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

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


session = dbconnect()

with open(r"uk-towns-sample.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for town in reader:
        addTown(session, town)
