from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, asc, desc

from .database import get_db
from .models import FDIProject, Company, Sector


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