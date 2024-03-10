import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DatabaseConnector:
    def __init__(self, database_url=None):
        if database_url is None:
            database_url = self.get_database_url_from_env()

        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

    @staticmethod
    def get_database_url_from_env():
        username = os.getenv("DB_USERNAME", "root")
        password = os.getenv("DB_PASSWORD", "password")
        host = os.getenv("DB_HOST", "localhost")
        database = os.getenv("DB_NAME", "default_database")

        return f"mysql+mysqlconnector://{username}:{password}@{host}/{database}"

if __name__ == "__main__":
    connector = DatabaseConnector()
    session = connector.Session()

    try:
        # Your database operations go here
        result = session.execute("SELECT * FROM results")
        print(result.fetchall())
    finally:
        session.close()
