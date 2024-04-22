import os

from dotenv import load_dotenv

load_dotenv()

PRODUCT_TABLE_NAME = os.environ.get("PRODUCT_TABLE_NAME", "sku")
PRODUCT_TAG_NAME = os.environ.get("PRODUCT_TAG_NAME", "offer")

CATEGORY_TAG_NAME = os.environ.get("CATEGORY_TAG_NAME", "category")
CATEGORY_MAIN_TAG_NAME = os.environ.get("CATEGORY_MAIN_TAG_NAME", "categories")

XML_PATH = os.environ.get("XML_PATH", "data.xml")
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 100))
SCHEMA_CONTENT = os.environ.get("SCHEMA_CONTENT", "public")

SLEEP_TIME = os.environ.get("SLEEP_TIME", 2)
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

DSL = {
    "dbname": os.environ.get("POSTGRES_DB", "postgres"),
    "user": os.environ.get("POSTGRES_USER", "postgres"),
    "password": os.environ.get("POSTGRES_PASSWORD", "1"),
    "host": os.environ.get("POSTGRES_HOST", "localhost"),
    "port": os.environ.get("POSTGRES_PORT", 5432),
}
