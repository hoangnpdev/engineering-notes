from typing import List, Dict, Any

from mini_cross.cross_table import Table


class ClickhouseTable(Table):

    @classmethod
    def new_table(cls, table_name, columns):
        pass

    def columns(self):
        pass

    def insert(self, rows: List[Dict[str, Any]]):
        pass

    def rows(self) -> List[Dict[str, Any]]:
        pass

    def size(self):
        pass

