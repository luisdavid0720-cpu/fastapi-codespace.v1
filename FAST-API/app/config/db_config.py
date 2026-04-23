import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("NEON_HOST"),
        port=os.getenv("NEON_PORT", "5432"),
        user=os.getenv("NEON_USER"),
        password=os.getenv("NEON_PASSWORD"),
        dbname=os.getenv("NEON_DBNAME"),
        sslmode="require"
    )