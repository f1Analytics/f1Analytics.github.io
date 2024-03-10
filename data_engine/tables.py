from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Result(Base):
    __tablename__ = "results"

    resultId = Column(Integer, primary_key=True)
    raceId = Column(Integer, ForeignKey("race.raceId"), nullable=False)
    driverId = Column(Integer, ForeignKey("driver.driverId"), nullable=False)
    constructorId = Column(Integer, ForeignKey("constructor.constructorId"), nullable=False)
    
    
