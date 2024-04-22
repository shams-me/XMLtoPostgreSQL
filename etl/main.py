import logging
from time import sleep

import psycopg2
from backoff import backoff
from config import (
    CATEGORY_MAIN_TAG_NAME,
    CATEGORY_TAG_NAME,
    CHUNK_SIZE,
    DSL,
    PRODUCT_TABLE_NAME,
    PRODUCT_TAG_NAME,
    SCHEMA_CONTENT,
    SLEEP_TIME,
    XML_PATH,
)
from models import Product
from postgres_loader import PostgresLoader
from xml_extractor import XMLExtractor

logging.basicConfig(level=logging.INFO)


@backoff()
def load_data(extractor: XMLExtractor, loader: PostgresLoader):

    for data in extractor.extract(
        model=Product, tag=PRODUCT_TAG_NAME, category_main_tag=CATEGORY_MAIN_TAG_NAME, category_tag=CATEGORY_TAG_NAME
    ):
        logging.info("Loading %s rows to %s table", len(data), PRODUCT_TABLE_NAME)
        loader.load_data(table_name=PRODUCT_TABLE_NAME, model=Product, data=data)
        logging.info("Loading %s rows to %s table is finished", len(data), PRODUCT_TABLE_NAME)

    logging.info("Loading data to %s table is finished", PRODUCT_TABLE_NAME)


@backoff()
def main():
    logging.info("ETL application is started")
    pg_connection = psycopg2.connect(**DSL)
    try:
        with pg_connection as conn:
            extractor = XMLExtractor(
                path_to_xml=XML_PATH,
                chunk_size=CHUNK_SIZE,
            )
            loader = PostgresLoader(conn=conn, schema=SCHEMA_CONTENT)
            while True:
                load_data(extractor=extractor, loader=loader)
                sleep(int(SLEEP_TIME))
                logging.info("Sleeping for %s seconds", SLEEP_TIME)
    finally:
        pg_connection.close()


if __name__ == "__main__":
    main()
