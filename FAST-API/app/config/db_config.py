import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("ep-mute-frost-aik454gz-pooler.c-4.us-east-1.aws.neon.tech"),
        port="5432",
        user=os.getenv(" neondb_owner"),
        password=os.getenv("npg_u8fxZahW0kEN"),
        dbname=os.getenv("neondb"),
        sslmode="require"
    )
