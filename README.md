# Steam Data Pipeline

A data pipeline project that collects, processes, and analyzes Steam game and achievement data using Airflow, dbt, and PostgreSQL.

## Features

- **Automated Data Collection:** Uses Airflow DAGs to fetch top 100 Steam games, player counts, achievement details, and achievement percentages.
- **Data Transformation:** dbt models for staging and marts, transforming raw data into analytics-ready tables.
- **PostgreSQL Storage:** All data is stored and processed in a PostgreSQL database.
- **Containerized Environment:** Easily reproducible with Docker Compose.

## Project Structure

```
.
├── dags/
│   ├── achievement_info_dag.py
│   ├── achievement_percentages_dag.py
│   ├── bootstrap_dag.py
│   ├── helper_func.py
│   ├── steam_api_func.py
│   ├── steamspy_dag.py
│   └── ...
├── dags/dbt/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── marts/
│   │   └── staging/
│   └── ...
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Setup & Run

1. **Clone the repository:**
    ```sh
    git clone https://github.com/kentyler96/steam_data_pipeline.git
    cd steam_data_pipeline
    ```

2. **Set your Steam API Key in Airflow Variables:**
   - Open Airflow UI (see below), go to Admin > Variables, and add `STEAM_API_KEY`.

3. **Start the pipeline:**
    ```sh
    docker compose up --build
    ```

4. **Access Airflow UI:**
    - Visit [http://localhost:8080](http://localhost:8080) in your browser.

5. **Trigger DAGs:**
    - Use the Airflow UI to trigger the DAGs for data ingestion and transformation.

### dbt Usage

- To run dbt models manually inside the Airflow container:
    ```sh
    docker exec -it <airflow-container-name> bash
    cd /opt/airflow/dbt
    dbt run
    dbt test
    ```

## Configuration

- Database connection and Airflow/dbt profiles are set up in `compose.yaml` and `dags/dbt/profiles/`.
- dbt models and sources are defined in `dags/dbt/models/` and corresponding `schema.yml` files.

## Project DAGs

- **bootstrap_dag:** Initializes all tables and loads initial data.
- **steamspy_dag:** Fetches top 100 games from SteamSpy.
- **achievement_info_dag:** Fetches achievement metadata for top games.
- **achievement_percentages_dag:** Fetches achievement percentages for top games.

## License

MIT License. See [LICENSE](LICENSE) for details.

---

**Resources:**
- [dbt Documentation](https://docs.getdbt.com/docs/introduction)
- [Airflow Documentation](https://airflow.apache.org/docs/)


achievement achievement
