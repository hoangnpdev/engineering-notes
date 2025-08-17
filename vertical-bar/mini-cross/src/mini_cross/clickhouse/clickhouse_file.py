from typing import List, Dict
from mini_cross.clickhouse.clickhouse_block import MetaBlock, IColumn


class ClickHouseFile:
    def __init__(self):
        pass

    @staticmethod
    def save_table(self, table_name, columns, table_metadata):
        pass

    @staticmethod
    def save_data(table_name, column_names, column_bytes, primary_index_bytes, column_marks_bytes):
        pass

    @staticmethod
    def load_metablock(table_name):
        # This should return a MetaBlock instance
        pass


    @staticmethod
    def destroy():
        pass




