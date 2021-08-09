from sqlalchemy import Integer, Column, String, Float, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

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

# Rides
class Journey(Base):
    __tablename__ = 'journey'
    id = Column(Integer, primary_key=True)
    # https://docs.sqlalchemy.org/en/13/orm/join_conditions.html#handling-multiple-join-paths

    # From
    from_town_id = Column(Integer, ForeignKey('town.id'))
    from_town = relation("Town", foreign_keys=[from_town_id])

    # To
    to_town_id = Column(Integer, ForeignKey("town.id"))
    to_town = relation("Town", foreign_keys=[to_town_id])
    
    # Price and Distance
    distance = Column(Float)
    number_of_passenges = Column(Integer)
    weight = Column(Float)
    price = Column(Float)

    # automatic timestamp
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return "<Journey(id='%i')>" % (self.id)


# A bunch of stuff to make the connection to the database work.
def dbconnect():
    engine = create_engine("mysql+pymysql://root:root@localhost/towns?charset=utf8mb4")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()