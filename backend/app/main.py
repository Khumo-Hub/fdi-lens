from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, extract, asc, desc, or_

from .database import get_db
from .models import FDIProject, Company, Sector, Country


app = FastAPI(
    title="FDI Lens API",
    description="API for the FDI Lens Global Investment Intelligence Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to the FDI Lens API"
    }


@app.get("/api/search")
def global_search(
    q: str = Query(
        ...,
        min_length=2,
        max_length=100
    ),
    limit: int = Query(
        default=5,
        ge=1,
        le=10
    ),
    db: Session = Depends(get_db)
):
    search_term = q.strip()

    if len(search_term) < 2:
        return {
            "query": search_term,
            "companies": [],
            "projects": [],
            "countries": [],
            "sectors": [],
        }

    pattern = f"%{search_term}%"

    companies = (
        db.query(Company)
        .filter(
            or_(
                Company.name.ilike(pattern),
                Company.industry.ilike(pattern),
                Company.description.ilike(pattern),
            )
        )
        .order_by(Company.name.asc())
        .limit(limit)
        .all()
    )

    countries = (
        db.query(Country)
        .filter(
            or_(
                Country.name.ilike(pattern),
                Country.code.ilike(pattern),
                Country.region.ilike(pattern),
            )
        )
        .order_by(Country.name.asc())
        .limit(limit)
        .all()
    )

    sectors = (
        db.query(Sector)
        .filter(
            or_(
                Sector.name.ilike(pattern),
                Sector.cluster.ilike(pattern),
            )
        )
        .order_by(Sector.name.asc())
        .limit(limit)
        .all()
    )

    source_country = aliased(Country)
    destination_country = aliased(Country)

    projects = (
        db.query(FDIProject)
        .join(Company)
        .join(Sector)
        .join(
            source_country,
            FDIProject.source_country_code
            == source_country.code
        )
        .join(
            destination_country,
            FDIProject.destination_country_code
            == destination_country.code
        )
        .filter(
            or_(
                Company.name.ilike(pattern),
                Company.industry.ilike(pattern),
                FDIProject.description.ilike(pattern),
                FDIProject.project_type.ilike(pattern),
                Sector.name.ilike(pattern),
                Sector.cluster.ilike(pattern),
                source_country.name.ilike(pattern),
                source_country.code.ilike(pattern),
                destination_country.name.ilike(pattern),
                destination_country.code.ilike(pattern),
            )
        )
        .order_by(
            FDIProject.announcement_date.desc()
        )
        .limit(limit)
        .all()
    )

    return {
        "query": search_term,
        "companies": [
            {
                "id": company.id,
                "name": company.name,
                "headquarters_country":
                    company.headquarters_country,
                "industry": company.industry,
            }
            for company in companies
        ],
        "projects": [
            {
                "id": project.id,
                "company": project.company.name,
                "source_country":
                    project.source_country_code,
                "destination_country":
                    project.destination_country_code,
                "sector": project.sector.name,
                "project_type": project.project_type,
                "capex_usd": project.capex_usd,
                "jobs_created": project.jobs_created,
                "announcement_date":
                    project.announcement_date,
                "status": project.status,
                "description": project.description,
            }
            for project in projects
        ],
        "countries": [
            {
                "code": country.code,
                "name": country.name,
                "region": country.region,
            }
            for country in countries
        ],
        "sectors": [
            {
                "id": sector.id,
                "name": sector.name,
                "cluster": sector.cluster,
            }
            for sector in sectors
        ],
    }


@app.get("/api/projects")
def get_projects(

    destination_country: str | None = None,
    source_country: str | None = None,
    sector: str | None = None,

    year_from: int | None = None,
    year_to: int | None = None,

    min_capex: float | None = None,
    max_capex: float | None = None,

    project_type: str | None = None,
    company_name: str | None = None,

    page: int = Query(
        default=1,
        ge=1
    ),

    page_size: int = Query(
        default=25,
        ge=1,
        le=100
    ),

    sort_by: str = "announcement_date",
    sort_order: str = "desc",

    db: Session = Depends(get_db)
):

    query = (
        db.query(FDIProject)
        .join(Company)
        .join(Sector)
    )

    # ---------------------------------
    # Country filters
    # ---------------------------------

    if destination_country:

        query = query.filter(
            FDIProject.destination_country_code
            == destination_country.upper()
        )

    if source_country:

        query = query.filter(
            FDIProject.source_country_code
            == source_country.upper()
        )

    # ---------------------------------
    # Sector filter
    # ---------------------------------

    if sector:

        query = query.filter(
            Sector.name.ilike(
                f"%{sector}%"
            )
        )

    # ---------------------------------
    # Year filters
    # ---------------------------------

    if year_from:

        query = query.filter(
            extract(
                "year",
                FDIProject.announcement_date
            ) >= year_from
        )

    if year_to:

        query = query.filter(
            extract(
                "year",
                FDIProject.announcement_date
            ) <= year_to
        )

    # ---------------------------------
    # Capital expenditure filters
    # ---------------------------------

    if min_capex is not None:

        query = query.filter(
            FDIProject.capex_usd
            >= min_capex
        )

    if max_capex is not None:

        query = query.filter(
            FDIProject.capex_usd
            <= max_capex
        )

    # ---------------------------------
    # Project type
    # ---------------------------------

    if project_type:

        query = query.filter(
            FDIProject.project_type.ilike(
                project_type
            )
        )

    # ---------------------------------
    # Company name search
    # ---------------------------------

    if company_name:

        query = query.filter(
            Company.name.ilike(
                f"%{company_name}%"
            )
        )

    # ---------------------------------
    # Total before pagination
    # ---------------------------------

    total = query.count()

    # ---------------------------------
    # Sorting
    # ---------------------------------

    sort_columns = {
        "announcement_date":
            FDIProject.announcement_date,

        "capex_usd":
            FDIProject.capex_usd,

        "jobs_created":
            FDIProject.jobs_created,

        "company":
            Company.name,

        "sector":
            Sector.name
    }

    sort_column = sort_columns.get(
        sort_by,
        FDIProject.announcement_date
    )

    if sort_order.lower() == "asc":

        query = query.order_by(
            asc(sort_column)
        )

    else:

        query = query.order_by(
            desc(sort_column)
        )

    # ---------------------------------
    # Pagination
    # ---------------------------------

    offset = (
        page - 1
    ) * page_size

    projects = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    # ---------------------------------
    # Format response
    # ---------------------------------

    items = []

    for project in projects:

        items.append({
            "id":
                project.id,

            "company":
                project.company.name,

            "source_country":
                project.source_country_code,

            "destination_country":
                project.destination_country_code,

            "sector":
                project.sector.name,

            "project_type":
                project.project_type,

            "capex_usd":
                project.capex_usd,

            "jobs_created":
                project.jobs_created,

            "announcement_date":
                project.announcement_date,

            "status":
                project.status,

            "description":
                project.description
        })

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "results_on_page": len(items),
        "items": items
    }


@app.get("/api/analytics/summary")
def get_analytics_summary(
    db: Session = Depends(get_db)
):

    total_projects = db.query(
        func.count(FDIProject.id)
    ).scalar()

    total_capex = db.query(
        func.sum(
            FDIProject.capex_usd
        )
    ).scalar() or 0

    total_jobs = db.query(
        func.sum(
            FDIProject.jobs_created
        )
    ).scalar() or 0

    countries_count = db.query(
        func.count(
            func.distinct(
                FDIProject.destination_country_code
            )
        )
    ).scalar()

    return {
        "total_projects":
            total_projects,

        "total_capex_usd":
            total_capex,

        "total_jobs":
            total_jobs,

        "countries_count":
            countries_count
    }

@app.get("/api/analytics/top-destinations")
def get_top_destinations(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):

    results = (
        db.query(
            FDIProject.destination_country_code.label("country"),
            func.count(FDIProject.id).label("project_count"),
            func.sum(FDIProject.capex_usd).label("total_capex_usd"),
            func.sum(FDIProject.jobs_created).label("total_jobs")
        )
        .group_by(
            FDIProject.destination_country_code
        )
        .order_by(
            func.count(FDIProject.id).desc()
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "country": row.country,
            "project_count": row.project_count,
            "total_capex_usd": row.total_capex_usd or 0,
            "total_jobs": row.total_jobs or 0
        }
        for row in results
    ]


@app.get("/api/analytics/top-sources")
def get_top_sources(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):

    results = (
        db.query(
            FDIProject.source_country_code.label("country"),
            func.count(FDIProject.id).label("project_count"),
            func.sum(FDIProject.capex_usd).label("total_capex_usd"),
            func.sum(FDIProject.jobs_created).label("total_jobs")
        )
        .group_by(
            FDIProject.source_country_code
        )
        .order_by(
            func.count(FDIProject.id).desc()
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "country": row.country,
            "project_count": row.project_count,
            "total_capex_usd": row.total_capex_usd or 0,
            "total_jobs": row.total_jobs or 0
        }
        for row in results
    ]


@app.get("/api/analytics/top-sectors")
def get_top_sectors(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):

    results = (
        db.query(
            Sector.name.label("sector"),
            func.count(FDIProject.id).label("project_count"),
            func.sum(FDIProject.capex_usd).label("total_capex_usd"),
            func.sum(FDIProject.jobs_created).label("total_jobs")
        )
        .join(
            FDIProject,
            FDIProject.sector_id == Sector.id
        )
        .group_by(
            Sector.name
        )
        .order_by(
            func.sum(FDIProject.capex_usd).desc()
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "sector": row.sector,
            "project_count": row.project_count,
            "total_capex_usd": row.total_capex_usd or 0,
            "total_jobs": row.total_jobs or 0
        }
        for row in results
    ]


@app.get("/api/analytics/trends")
def get_investment_trends(
    db: Session = Depends(get_db)
):

    month = func.strftime(
        "%Y-%m",
        FDIProject.announcement_date
    )

    results = (
        db.query(
            month.label("month"),
            func.count(FDIProject.id).label("project_count"),
            func.sum(FDIProject.capex_usd).label("total_capex_usd"),
            func.sum(FDIProject.jobs_created).label("total_jobs")
        )
        .group_by(month)
        .order_by(month)
        .all()
    )

    return [
        {
            "month": row.month,
            "project_count": row.project_count,
            "total_capex_usd": row.total_capex_usd or 0,
            "total_jobs": row.total_jobs or 0
        }
        for row in results
    ]



@app.get("/api/analytics/map")
def get_investment_map(
    db: Session = Depends(get_db)
):

    results = (
        db.query(
            Country.code.label(
                "country_code"
            ),
            Country.name.label(
                "country_name"
            ),
            Country.region.label(
                "region"
            ),
            Country.latitude.label(
                "latitude"
            ),
            Country.longitude.label(
                "longitude"
            ),
            func.count(
                FDIProject.id
            ).label(
                "project_count"
            ),
            func.sum(
                FDIProject.capex_usd
            ).label(
                "total_capex_usd"
            ),
            func.sum(
                FDIProject.jobs_created
            ).label(
                "total_jobs"
            ),
        )
        .join(
            FDIProject,
            FDIProject.destination_country_code
            == Country.code
        )
        .filter(
            Country.latitude.isnot(None),
            Country.longitude.isnot(None),
        )
        .group_by(
            Country.code,
            Country.name,
            Country.region,
            Country.latitude,
            Country.longitude,
        )
        .order_by(
            func.count(
                FDIProject.id
            ).desc()
        )
        .all()
    )


    return [
        {
            "country_code":
                row.country_code,

            "country_name":
                row.country_name,

            "region":
                row.region,

            "latitude":
                row.latitude,

            "longitude":
                row.longitude,

            "project_count":
                row.project_count,

            "total_capex_usd":
                row.total_capex_usd or 0,

            "total_jobs":
                row.total_jobs or 0,
        }

        for row in results
    ]