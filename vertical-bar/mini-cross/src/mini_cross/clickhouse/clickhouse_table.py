from typing import List, Dict, Any

from mini_cross.cross_table import Table
from mini_cross.clickhouse.clickhouse_file import ClickHouseFile
from mini_cross.clickhouse.clickhouse_block import MetaBlock, IColumn
from mini_cross.clickhouse.clickhouse_idx import PrimaryIndex, ColumnMark
from mini_cross.clickhouse.config import CLICKHOUSE_CONFIG
from mini_cross.clickhouse import common_util
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
        metadata = ClickHouseFile.load_metablock(self.table_name)
        metablock = MetaBlock.from_bytes(metadata)
        return metablock.columns()
    
    def keys(self):
        metadata = ClickHouseFile.load_metablock(self.table_name)
        metablock = MetaBlock.from_bytes(metadata)
        return metablock.keys()
        

    def insert(self, rows: List[Dict[str, Any]]):
        # construct table columns (column list from columns function, byte format) from rows param
        column_names = self.columns()
        key_names = self.keys()
        column_data = {name: IColumn() for name in column_names}
        column_marks = {name: ColumnMark() for name in column_names}
        primary_index = PrimaryIndex()
        # sort rows by key names
        rows.sort(key=lambda x: tuple(x[name] for name in key_names))
        for batch in common_util.chunk_list(rows, CLICKHOUSE_CONFIG.INDEX_GRANULARITY):  # Process rows in chunks
            # add values of keys of first row in batch to primary index
            if batch:
                primary_index.add_key(tuple(batch[0][name] for name in key_names))
            last_byte_positions = {name: 0 for name in column_names}
            for row in batch:
                for name in column_names:
                    if name in row:
                        last_byte_positions[name] = column_data[name].append(row[name])
                    else:
                        last_byte_positions[name] = column_data[name].append(None)
            # add marks for each column
            for name in column_names:
                column_marks[name].add_mark(last_byte_positions[name])
        # save table IColumns using ClickHouseFile
        column_bytes = [col.to_bytes() for col in column_data.values()]
        primary_index_bytes = primary_index.to_bytes()
        column_marks_bytes = [mark.to_bytes() for mark in column_marks.values()]
        ClickHouseFile.save_data(self.table_name, column_bytes, primary_index_bytes, column_marks_bytes)
        # trigger merging
        self.merge_partitions()


    def merge_partitions(self):
        # todo
        pass

    def rows(self) -> List[Dict[str, Any]]:
        pass

    def size(self):
        pass

