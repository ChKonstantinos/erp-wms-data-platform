# ERP/WMS Data Platform

An end-to-end Data Engineering portfolio project that simulates the integration of ERP sales data and Warehouse Management System (WMS) operations.

The platform demonstrates data ingestion, validation, transformation, orchestration, and analytics using Python, PostgreSQL, Apache Airflow, dbt, Docker, and Power BI.

## Project Objectives

- Simulate ERP and WMS business data.
- Build a structured Bronze, Silver, and Gold data architecture.
- Implement data validation and quality checks.
- Automate pipeline execution using Apache Airflow.
- Transform analytical datasets using dbt.
- Support business reporting and KPI monitoring.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data generation, ingestion, and pipeline processing |
| PostgreSQL | Data storage and SQL transformations |
| Apache Airflow | Pipeline orchestration and monitoring |
| dbt | Gold-layer analytical transformations and testing |
| Docker | Containerized development environment |
| pytest | Automated Python testing |
| GitHub Actions | Continuous integration checks |
| Power BI | Business intelligence and reporting |

## Data Architecture

The platform follows a three-layer data architecture.

**Bronze Layer**

Stores ingested operational data from simulated ERP and WMS systems.

**Silver Layer**

Applies validation, cleaning, and transformation logic to prepare reliable operational datasets.

**Gold Layer**

Provides analytical models and business KPIs, including order fulfillment, inventory availability, and pipeline monitoring.

## Pipeline Orchestration

Apache Airflow coordinates the main pipeline stages:

1. Pipeline audit initialization
2. Bronze data ingestion
3. Silver picking transformation
4. Silver stock transformation
5. dbt Gold model execution

Pipeline execution results are recorded in PostgreSQL for monitoring and troubleshooting.

## Analytics

The Gold layer supports reporting on:

- Order fulfillment performance
- Ordered versus picked quantities
- Shortages and overpicking
- Inventory availability and stock status
- Pipeline execution monitoring

Power BI is used to visualize analytical results.

## Repository Structure

```text
erp-wms-data-platform/
├── .github/workflows/   # CI configuration
├── airflow/              # Airflow DAG and Docker configuration
├── docker/               # Database initialization
├── erp_wms_dbt/          # dbt models and tests
├── sql/                  # Database schema and SQL transformations
├── src/                  # Python pipeline modules
├── tests/                # Automated tests
├── compose.yaml          # ERP/WMS Docker services
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Configuration

The project uses environment variables for database credentials and local configuration.

Copy `.env.example` to `.env` and replace the placeholder values with your local credentials.

The `.env` file is excluded from version control.

## Development Status

The core data pipeline, Airflow orchestration, dbt models, and Power BI reporting have been implemented and tested in the local development environment.

GitHub Actions CI configuration has been added. Further automated checks and deployment improvements are planned.

## Future Improvements

- Expand CI coverage with Python and dbt tests.
- Improve environment setup documentation and reproducibility.
- Extend data quality monitoring.
- Refine pipeline deployment and configuration.

## Project Scope

This is a learning and portfolio project based on simulated operational data. It is not a production deployment.