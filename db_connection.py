import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DSN = os.getenv("DB_DSN")

def connect_to_db():
    try:
        if not USER or not PASSWORD or not DSN:
            raise ValueError("Variáveis de ambiente DB_USER, DB_PASSWORD ou DB_DSN estão ausentes.")

        conn = oracledb.connect(
            user=USER,
            password=PASSWORD,
            dsn=DSN,
        )
        return conn
    except Exception as error:
        print("Database connection error:", error)
        return None
