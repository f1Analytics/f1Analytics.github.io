from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Define your SQLAlchemy base
Base = declarative_base()

if __name__ == "__main__":
    # Your code goes here
    engine = create_engine("sqlite:///testf1.db", echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
