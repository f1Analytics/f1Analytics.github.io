from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Create a declarative base class
Base = declarative_base()

class Circuit(Base):
    __tablename__ = 'circuits'
    
    circuit_id = Column(String, primary_key=True)
    circuit_name = Column(String)
    location = Column(String)
    country = Column(String)
    races = relationship("Race", back_populates="circuit")

class Race(Base):
    __tablename__ = 'races'
    
    race_id = Column(Integer, primary_key=True)
    year = Column(Integer)
    round = Column(Integer)
    circuit_id = Column(String, ForeignKey('circuits.circuit_id'))
    circuit = relationship("Circuit", back_populates="races")
    results = relationship("Result", back_populates="race")

class Driver(Base):
    __tablename__ = 'drivers'
    
    driver_id = Column(String, primary_key=True)
    driver_ref = Column(String)
    number = Column(Integer)
    code = Column(String)
    forename = Column(String)
    surname = Column(String)
    nationality = Column(String)
    dob = Column(DateTime)
    results = relationship("Result", back_populates="driver")

class Constructor(Base):
    __tablename__ = 'constructors'
    
    constructor_id = Column(String, primary_key=True)
    constructor_ref = Column(String)
    name = Column(String)
    nationality = Column(String)
    results = relationship("Result", back_populates="constructor")

class Result(Base):
    __tablename__ = 'results'
    
    result_id = Column(Integer, primary_key=True)
    race_id = Column(Integer, ForeignKey('races.race_id'))
    driver_id = Column(String, ForeignKey('drivers.driver_id'))
    constructor_id = Column(String, ForeignKey('constructors.constructor_id'))
    position = Column(Integer)
    points = Column(Integer)
    race = relationship("Race", back_populates="results")
    driver = relationship("Driver", back_populates="results")
    constructor = relationship("Constructor", back_populates="results")

class Lap(Base):
    __tablename__ = "laps"

    lap_number = Column(Integer)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    race_id = Column(Integer, ForeignKey("races.race_id"))
    position = Column(Integer)

    driver = relationship("Driver", back_populates="laps")
    race = relationship("Race", back_populates="laps")
    