from typing import List

from mini_cross.clickhouse.clickhouse_table import ClickhouseTable
from mini_cross.clickhouse.clickhouse_file import ClickHouseFile
from mini_cross.cross_table import TableRef
from mini_cross.postgres.postgres_table import PostgresTable
from mini_cross.postgres.postgres_file import PostgresFile


# handle database operator at row, table level
class MiniCross:

    @staticmethod
    def create_postgres_table(table_name, columns: List[str]):
        # convert column_name to bytes
        PostgresTable.new_table(table_name, columns)

    @staticmethod
    def load_postgres_table(table_name: str) -> PostgresTable:
        return PostgresTable(table_name)

    @staticmethod
    def create_clickhouse_table(table_name, columns: List[str], keys: List[str]):
        ClickhouseTable.new_table(table_name, columns, keys)

    @staticmethod
    def load_clickhouse_table(table_name):
        return ClickhouseTable(table_name)

    @staticmethod
    def load_table_ref(table_name: str) -> TableRef:
        return TableRef(MiniCross.load_postgres_table(table_name))

    @staticmethod
    def destroy():
        PostgresFile.destroy()
        ClickHouseFile.destroy()



