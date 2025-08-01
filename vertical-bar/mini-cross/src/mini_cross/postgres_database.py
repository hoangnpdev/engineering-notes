from typing import List
from mini_cross.postgres_table import Table


# handle database operator at row, table level
class MiniPostgres:

    @staticmethod
    def create_table(table_name, columns: List[str]):
        # convert column_name to bytes
        Table.new_table(table_name, columns)

    @staticmethod
    def load_table(table_name: str) -> Table:
        return Table(table_name)



