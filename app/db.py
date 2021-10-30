from sqlmodel import SQLModel, create_engine

from config import Settings

engine = create_engine(f"sqlite:///{Settings.FILEPATH_DB}")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
