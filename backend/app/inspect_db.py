from .database import SessionLocal
from .models import Country, Sector, Company, FDIProject


def inspect_database():

    db = SessionLocal()

    try:
        print("\nFDI LENS DATABASE SUMMARY")
        print("-------------------------")

        print(f"Countries: {db.query(Country).count()}")
        print(f"Sectors: {db.query(Sector).count()}")
        print(f"Companies: {db.query(Company).count()}")
        print(f"FDI Projects: {db.query(FDIProject).count()}")

        print("\nSAMPLE PROJECTS")
        print("---------------")

        projects = db.query(FDIProject).limit(5).all()

        for project in projects:

            print()
            print(f"Project ID: {project.id}")
            print(f"Company: {project.company.name}")
            print(f"Source: {project.source_country_code}")
            print(f"Destination: {project.destination_country_code}")
            print(f"Sector: {project.sector.name}")
            print(f"Capex: ${project.capex_usd:,.2f}")
            print(f"Jobs: {project.jobs_created:,}")
            print(f"Type: {project.project_type}")
            print(f"Date: {project.announcement_date}")
            print(f"Status: {project.status}")

    finally:
        db.close()


if __name__ == "__main__":
    inspect_database()