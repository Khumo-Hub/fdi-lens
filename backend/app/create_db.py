from .database import Base, engine
from . import models


def create_database():
    print("Creating FDI Lens database...")

    Base.metadata.create_all(bind=engine)

    print("Database created successfully.")


if __name__ == "__main__":
    create_database()