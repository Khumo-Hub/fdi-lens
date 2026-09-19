from datetime import date, datetime

from sqlalchemy import (
    String,
    Integer,
    Float,
    Text,
    Date,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    headquarters_country: Mapped[str | None] = mapped_column(
        String(3),
        nullable=True
    )

    industry: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    website: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    projects: Mapped[list["FDIProject"]] = relationship(
        back_populates="company"
    )


class Sector(Base):
    __tablename__ = "sectors"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    cluster: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    projects: Mapped[list["FDIProject"]] = relationship(
        back_populates="sector"
    )


class Country(Base):
    __tablename__ = "countries"

    code: Mapped[str] = mapped_column(
        String(3),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    region: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    income_group: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )


class FDIProject(Base):
    __tablename__ = "fdi_projects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False
    )

    source_country_code: Mapped[str] = mapped_column(
        ForeignKey("countries.code"),
        nullable=False
    )

    destination_country_code: Mapped[str] = mapped_column(
        ForeignKey("countries.code"),
        nullable=False
    )

    sector_id: Mapped[int] = mapped_column(
        ForeignKey("sectors.id"),
        nullable=False
    )

    project_type: Mapped[str | None] = mapped_column(
        String(50)
    )

    capex_usd: Mapped[float | None] = mapped_column(
        Float
    )

    jobs_created: Mapped[int | None] = mapped_column(
        Integer
    )

    announcement_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="announced"
    )

    description: Mapped[str | None] = mapped_column(
        Text
    )

    source_url: Mapped[str | None] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    company: Mapped["Company"] = relationship(
        back_populates="projects"
    )

    sector: Mapped["Sector"] = relationship(
        back_populates="projects"
    )