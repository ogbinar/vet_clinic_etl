import duckdb
import logging

class Loader:
    def __init__(self, database):
        self.database = database

    def to_duckdb(self, df):
        try:
            con = duckdb.connect(database=self.database)
            con.execute("CREATE TABLE IF NOT EXISTS vet_clinics AS SELECT * FROM df")
            logging.info(f"Data loaded into {self.database} successfully")
        except Exception as e:
            logging.error(f"Error loading data into DuckDB: {e}")
