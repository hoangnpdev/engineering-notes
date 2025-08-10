from typing import List, Dict, Any

from mini_cross.cross_table import Table
"""
A separate primary.idx file has the value of the primary key for each N-th row (index_granularity).
Also, for each column, we have column.mrk files with "marks", which are offsets (byte position) 
    to each N-th row in the data file. this one to deal compression requirement.
    
ClickHouse is not suitable for a high load of simple point queries, 
because the entire range with index_granularity rows must be read for each key, 
and the entire compressed block must be decompressed for each column
"""


class ClickhouseTable(Table):

    @classmethod
    def new_table(cls, table_name, columns):
        pass

    def columns(self):
        pass

    def insert(self, rows: List[Dict[str, Any]]):
        # todo
        pass

    def merge_partitions(self):
        # todo
        pass

    def rows(self) -> List[Dict[str, Any]]:
        pass

    def size(self):
        pass

