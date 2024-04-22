# ETL (xml > postgreSQL)

## Description

This project is an ETL pipeline that extracts data from xml files, transforms it and loads it into a postgreSQL
database.

## Installation

1. Clone the repository

```bash
git clone https://github.com/shams-me/XMLtoPostgreSQL.git
```

2. Change .env.example to .env and fill in the required fields

| Field                  | Description                                                       |
|------------------------|-------------------------------------------------------------------|
| POSTGRES_DB            | Database name                                                     |
| POSTGRES_USER          | Database user                                                     |
| POSTGRES_PASSWORD      | Database password                                                 |
| POSTGRES_HOST          | Database host                                                     |
| POSTGRES_PORT          | Database port                                                     |
| SCHEMA_CONTENT         | Schema of the database                                            |
| PRODUCT_TABLE_NAME     | Name of the table to store the product data                       |
| PRODUCT_TAG_NAME       | Name of the tag that contains the product data inside XML file    |
| CATEGORY_MAIN_TAG_NAME | Name of the tag that contains the categories data inside XML file |
| CATEGORY_TAG_NAME      | Name of the tag that contains the category data inside XML file   |
| XML_PATH               | Path to the xml files                                             |
| CHUNK_SIZE             | Number of rows to insert in a single query                        |
| SLEEP_TIME             | Time to wait before inserting the next chunk of data              |
| LOG_LEVEL              | Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)                 |

3. Run docker compose

```bash
docker-compose up -d --build
```

# NOTE
- PDM wasn't used because it's a matter of personal preference. However, in real projects, using PDM/Poetry, and so on, is not difficult
