import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("ep-young-sunset-aid708e7-pooler.c-4.us-east-1.aws.neon.tech"),
        port="5432",
        user=os.getenv("neondb_owner"),
        password=os.getenv("npg_M8kwjLFHVdN7"),
        dbname=os.getenv("neondb"),
        sslmode="require"
    )
