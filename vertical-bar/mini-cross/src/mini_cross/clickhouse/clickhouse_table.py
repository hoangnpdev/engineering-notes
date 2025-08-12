from typing import List, Dict, Any

from mini_cross.cross_table import Table
from mini_cross.clickhouse.clickhouse_file import ClickHouseFile
from mini_cross.clickhouse.clickhouse_block import MetaBlock
"""
A separate primary.idx file has the value of the primary key for each N-th row (index_granularity).
Also, for each column, we have column.mrk files with "marks", which are offsets (byte position) 
    to each N-th row in the data file. this one to deal compression requirement.
    
ClickHouse is not suitable for a high load of simple point queries, 
because the entire range with index_granularity rows must be read for each key, 
and the entire compressed block must be decompressed for each column
"""


class ClickhouseTable(Table):

    def __init__(self, table_name):
        self.table_name = table_name

    @classmethod
    def new_table(cls, table_name, columns, keys):
        metadata = MetaBlock(columns, keys)
        ClickHouseFile.save_table(table_name, columns, metadata.to_bytes())

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

