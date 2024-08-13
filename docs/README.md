# Vet Clinic ETL Pipeline

This project is an ETL pipeline for fetching, transforming, and loading vet clinic data from the Google Maps API into a DuckDB database.

- Community: https://DataEngineering.PH
- Meetup Link: https://www.meetup.com/data-engineering-pilipinas/events/302686497/
- Presentation slides: https://docs.google.com/presentation/d/1x9WdIHYcRm5iIZf5BFbgcNOfwG3q9dsq5cS1CP0Hl-o/edit?usp=sharing

## Setup

1. **Clone the repository**:
   ```sh
   git clone <repository_url>
   cd vet_clinic_etl
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure the API keys and settings**:
   - Edit the `config/config.yaml` file with your API key and other configuration settings.
   - Example:
     ```yaml
     google_maps_api_key: "YOUR_API_KEY"
     location: 
       latitude: 14.5726107
       longitude: 121.0413941
     radius: 1000
     duckdb:
       database: "vet_clinics.db"
     ```

4. **Run the ETL process**:
   ```sh
   python main.py
   ```

5. **Install and setup Metabase or DuckDB or DBeaver (or just use Python)**
