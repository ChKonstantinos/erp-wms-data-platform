import os
import psycopg
from dotenv import load_dotenv
from pathlib import Path


def get_connection():

    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(BASE_DIR / ".env")

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    conn = psycopg.connect(
        host = db_host,
        port = db_port,
        dbname = db_name,
        user = db_user,
        password = db_password
    )

    return conn

if __name__ == "__main__":

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT current_database();")
            result = cursor.fetchone()
            print(result)