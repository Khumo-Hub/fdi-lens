import random
from datetime import date, timedelta

from faker import Faker

from .country_coordinates import COUNTRY_COORDINATES

from .database import SessionLocal
from .models import Country, Sector, Company, FDIProject


fake = Faker()


COUNTRIES = [
    ("ZAF", "South Africa", "Sub-Saharan Africa"),
    ("USA", "United States", "North America"),
    ("GBR", "United Kingdom", "Europe"),
    ("DEU", "Germany", "Europe"),
    ("FRA", "France", "Europe"),
    ("CHN", "China", "East Asia"),
    ("JPN", "Japan", "East Asia"),
    ("KOR", "South Korea", "East Asia"),
    ("IND", "India", "South Asia"),
    ("BRA", "Brazil", "Latin America"),
    ("CAN", "Canada", "North America"),
    ("AUS", "Australia", "Oceania"),
    ("ITA", "Italy", "Europe"),
    ("ESP", "Spain", "Europe"),
    ("NLD", "Netherlands", "Europe"),
    ("BEL", "Belgium", "Europe"),
    ("CHE", "Switzerland", "Europe"),
    ("SWE", "Sweden", "Europe"),
    ("NOR", "Norway", "Europe"),
    ("DNK", "Denmark", "Europe"),
    ("FIN", "Finland", "Europe"),
    ("POL", "Poland", "Europe"),
    ("TUR", "Turkey", "Europe"),
    ("SAU", "Saudi Arabia", "Middle East"),
    ("ARE", "United Arab Emirates", "Middle East"),
    ("ISR", "Israel", "Middle East"),
    ("EGY", "Egypt", "North Africa"),
    ("MAR", "Morocco", "North Africa"),
    ("NGA", "Nigeria", "Sub-Saharan Africa"),
    ("KEN", "Kenya", "Sub-Saharan Africa"),
    ("GHA", "Ghana", "Sub-Saharan Africa"),
    ("ETH", "Ethiopia", "Sub-Saharan Africa"),
    ("TZA", "Tanzania", "Sub-Saharan Africa"),
    ("MOZ", "Mozambique", "Sub-Saharan Africa"),
    ("BWA", "Botswana", "Sub-Saharan Africa"),
    ("NAM", "Namibia", "Sub-Saharan Africa"),
    ("ZMB", "Zambia", "Sub-Saharan Africa"),
    ("AGO", "Angola", "Sub-Saharan Africa"),
    ("MEX", "Mexico", "Latin America"),
    ("ARG", "Argentina", "Latin America"),
    ("CHL", "Chile", "Latin America"),
    ("COL", "Colombia", "Latin America"),
    ("PER", "Peru", "Latin America"),
    ("SGP", "Singapore", "Southeast Asia"),
    ("MYS", "Malaysia", "Southeast Asia"),
    ("THA", "Thailand", "Southeast Asia"),
    ("VNM", "Vietnam", "Southeast Asia"),
    ("IDN", "Indonesia", "Southeast Asia"),
    ("NZL", "New Zealand", "Oceania"),
    ("IRL", "Ireland", "Europe"),
]


SECTORS = [
    ("Automotive", "Advanced Manufacturing"),
    ("Renewable Energy", "Energy"),
    ("Oil and Gas", "Energy"),
    ("Mining", "Natural Resources"),
    ("Information Technology", "Technology"),
    ("Semiconductors", "Technology"),
    ("Telecommunications", "Technology"),
    ("Financial Services", "Services"),
    ("Business Services", "Services"),
    ("Food and Beverages", "Consumer Goods"),
    ("Textiles and Apparel", "Consumer Goods"),
    ("Pharmaceuticals", "Life Sciences"),
    ("Healthcare", "Life Sciences"),
    ("Electronics", "Advanced Manufacturing"),
    ("Chemicals", "Industrial"),
    ("Construction", "Infrastructure"),
    ("Logistics", "Transport"),
    ("Aerospace", "Advanced Manufacturing"),
    ("Agriculture", "Agribusiness"),
    ("Data Centres", "Digital Infrastructure"),
]


PROJECT_TYPES = [
    "Greenfield",
    "Expansion",
]


STATUSES = [
    "announced",
    "confirmed",
    "operational",
]


def random_date():
    start = date(2024, 1, 1)
    end = date(2026, 9, 1)

    difference = end - start

    return start + timedelta(
        days=random.randint(0, difference.days)
    )


def seed_database():

    db = SessionLocal()

    try:
        existing_projects = db.query(FDIProject).count()

        if existing_projects > 0:
            print(
                f"Database already contains "
                f"{existing_projects} FDI projects."
            )
            print("Seed process stopped to prevent duplicates.")
            return

        print("Starting FDI Lens database seeding...")
        print()

        # -------------------------------------
        # 1. Countries
        # -------------------------------------

        countries = []

        for code, name, region in COUNTRIES:

            coordinates = COUNTRY_COORDINATES.get(
                code
            )

            latitude = None
            longitude = None

            if coordinates:
                latitude, longitude = coordinates

            country = Country(
                code=code,
                name=name,
                region=region,
                latitude=latitude,
                longitude=longitude,
            )

            db.add(country)
            countries.append(country)

        db.commit()

        print(f"Countries created: {len(countries)}")

        # -------------------------------------
        # 2. Sectors
        # -------------------------------------

        sectors = []

        for name, cluster in SECTORS:

            sector = Sector(
                name=name,
                cluster=cluster
            )

            db.add(sector)
            sectors.append(sector)

        db.commit()

        print(f"Sectors created: {len(sectors)}")

        # -------------------------------------
        # 3. Companies
        # -------------------------------------

        companies = []

        for _ in range(250):

            headquarters = random.choice(countries)
            industry = random.choice(sectors)

            company_name = fake.unique.company()

            company = Company(
                name=company_name,
                headquarters_country=headquarters.code,
                industry=industry.name,
                website=fake.url(),
                description=(
                    f"{company_name} operates in the "
                    f"{industry.name} sector."
                )
            )

            db.add(company)
            companies.append(company)

        db.commit()

        print(f"Companies created: {len(companies)}")

        # -------------------------------------
        # 4. FDI Projects
        # -------------------------------------

        projects_created = 0

        for _ in range(500):

            company = random.choice(companies)
            sector = random.choice(sectors)

            source_country = next(
                country
                for country in countries
                if country.code == company.headquarters_country
            )

            possible_destinations = [
                country
                for country in countries
                if country.code != source_country.code
            ]

            destination_country = random.choice(
                possible_destinations
            )

            capex = round(
                random.uniform(
                    5_000_000,
                    2_000_000_000
                ),
                2
            )

            jobs = random.randint(
                50,
                5000
            )

            project_type = random.choice(
                PROJECT_TYPES
            )

            status = random.choices(
                STATUSES,
                weights=[50, 30, 20],
                k=1
            )[0]

            announcement_date = random_date()

            description = (
                f"{company.name} announced a "
                f"{project_type.lower()} investment "
                f"in {destination_country.name} "
                f"in the {sector.name} sector. "
                f"The project represents an estimated "
                f"capital investment of "
                f"${capex:,.0f} and is expected "
                f"to create approximately "
                f"{jobs:,} jobs."
            )

            project = FDIProject(
                company_id=company.id,
                source_country_code=source_country.code,
                destination_country_code=destination_country.code,
                sector_id=sector.id,
                project_type=project_type,
                capex_usd=capex,
                jobs_created=jobs,
                announcement_date=announcement_date,
                status=status,
                description=description,
                source_url=None
            )

            db.add(project)

            projects_created += 1

        db.commit()

        print(
            f"FDI projects created: "
            f"{projects_created}"
        )

        print()
        print("--------------------------------")
        print("FDI Lens database seeded successfully!")
        print("--------------------------------")

    except Exception as error:

        db.rollback()

        print("An error occurred while seeding:")
        print(error)

    finally:

        db.close()


if __name__ == "__main__":
    seed_database()
