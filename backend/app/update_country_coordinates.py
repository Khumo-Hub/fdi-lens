from .database import SessionLocal
from .models import Country
from .country_coordinates import COUNTRY_COORDINATES


def update_country_coordinates():
    db = SessionLocal()

    try:
        countries = db.query(Country).all()

        updated = 0
        skipped = 0

        for country in countries:
            coordinates = COUNTRY_COORDINATES.get(
                country.code
            )

            if not coordinates:
                skipped += 1
                continue

            latitude, longitude = coordinates

            country.latitude = latitude
            country.longitude = longitude

            updated += 1

        db.commit()

        print(
            f"Country coordinates updated: {updated}"
        )

        print(
            f"Countries skipped: {skipped}"
        )

    except Exception as error:
        db.rollback()

        print(
            "Could not update country coordinates."
        )

        print(error)

    finally:
        db.close()


if __name__ == "__main__":
    update_country_coordinates()