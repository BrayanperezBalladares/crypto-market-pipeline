# Crypto Market Intelligence Pipeline

End-to-end data pipeline that ingests cryptocurrency market data
from CoinGecko API, transforms it into business metrics, and
serves an auto-updating analytics dashboard.

## Status
🚧 In progress — Week 1: Extraction layer

## Architecture
_Diagram coming in Week 3_
CoinGecko API → Airflow DAG → GCS (raw) → BigQuery → dbt → Looker Studio

## Stack
| Layer | Tool |
|---|---|
| Orchestration | Apache Airflow 2.9 |
| Raw storage | Google Cloud Storage |
| Warehouse | BigQuery |
| Transformation | dbt Core |
| Visualization | Looker Studio |
| Language | Python 3.11 |

## Project structure
crypto-market-pipeline/
├── dags/                        # Airflow DAGs
├── extractors/                  # CoinGecko API extraction logic
├── loaders/                     # GCS and BigQuery loaders
├── transforms/                  # dbt project
│   ├── models/
│   │   ├── staging/             # Clean and type raw data
│   │   ├── intermediate/        # Joins and calculations
│   │   └── marts/               # Business metrics
│   └── tests/                   # Custom dbt tests
├── docs/
│   └── architecture/            # Diagrams and technical decisions
├── docker-compose.yml           # Airflow local setup
├── requirements.txt
└── .env.example                 # Environment variables template

## Data layers
| Layer | Description |
|---|---|
| raw | JSON as-is from CoinGecko API, stored in GCS |
| staging | Cleaned, typed, deduplicated in BigQuery |
| intermediate | Joins and calculated fields |
| marts | Business metrics ready for analysis |

## Data quality
dbt tests run on every layer. Pipeline stops if any validation fails:
- `not_null` on critical columns
- `unique` on coin IDs
- Price and volume must be greater than zero

## Key decisions & trade-offs
| Decision | Reason |
|---|---|
| GCS as raw layer | Allows reprocessing without re-calling the API |
| Partitioned tables in BigQuery | Cost optimization on large date ranges |
| dbt tests before marts | No bad data reaches the final layer |
| Airflow on local Docker | Zero cost, uses existing headless server |

## Setup
_Coming soon — Week 1_

## Dashboard
_Coming soon — Week 3_
