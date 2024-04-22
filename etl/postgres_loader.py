from psycopg2.extensions import connection
from psycopg2.extras import execute_batch
from pydantic import BaseModel


class PostgresLoader:
    def __init__(self, conn: connection, schema: str = "public") -> None:
        self.pg_conn = conn
        self.schema = schema

    def load_data(self, table_name: str, model: type[BaseModel], data: list[type[BaseModel]]) -> None:
        """This function inserts data to database.
        Args:
            table_name (str): The name of the table to insert data into.
            model (BaseModel): The Pydantic model that represents the table schema.
            data (List[BaseModel]): The data to be inserted into the table.

        Returns: None
        """
        column_names = model.model_fields.keys()
        columns = ",".join(name for name in column_names)

        batch_data_values = [
            tuple(getattr(row, column).__str__() if getattr(row, column) else None for column in column_names)
            for row in data
        ]
        placeholders = ",".join(["%s"] * len(column_names))

        stmt = f"INSERT INTO {self.schema}.{table_name} ({columns}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"

        self.__batch_insert(stmt, batch_data_values)
        self.pg_conn.commit()

    def __batch_insert(self, stmt: str, data: list[tuple]) -> None:
        cur = self.pg_conn.cursor()
        execute_batch(cur, stmt, data, page_size=100)
        cur.close()
