from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pandas as pd

# Define your SQLAlchemy base
Base = declarative_base()


class F1Base(Base):
    __abstract__ = True

    def to_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    @classmethod
    def from_df(cls, df):
        return [cls(**row) for _, row in df.iterrows()]


# Define your SQLAlchemy models
class GP(F1Base):
    __tablename__ = "gp"
    id = Column(Integer, primary_key=True)
    gp_name = Column(String)

    lap = relationship("Lap", backref="gp")
    driver = relationship("Driver", backref="gp")


class Lap(F1Base):
    __tablename__ = "laps"
    id = Column(Integer, primary_key=True)
    gp_id = Column(Integer, ForeignKey("gp.id"))
    lap_number = Column(Integer)
    lap_time = Column(Time)

    driver = relationship("Driver", backref="lap")


class Driver(F1Base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbr = Column(String)

    parent = relationship("Parent", back_populates="children")


class Constructor(F1Base):
    __tablename__ = "constructor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbreviation = Column(String)


def get_data_from_csv():
    df = pd.read_csv("data.csv")
    return df


if __name__ == "__main__":
    # Your code goes here
    engine = create_engine("sqlite:///testf1.db", echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    data = get_data_from_csv()
