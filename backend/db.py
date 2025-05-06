# import postgresql driver
import psycopg2
import os
from dotenv import load_dotenv


# tell python to load all available from .env into os.environ
load_dotenv()
# Retrieves DB_URL securely from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# defines a reusable function to get a connection to the database
def get_connection():
    return psycopg2.connect(DATABASE_URL)
