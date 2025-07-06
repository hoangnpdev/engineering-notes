from typing import List
from postgres_io.postgres_io import FileManager
from buffer.buffer_manager import BufferManager


class QueryExecutor:

    @staticmethod
    def create_table(table_name, columns: List[str]):
        # convert column_name to bytes
        first_page = MetaPage.new_page(columns)
        FileManager.save_table(first_page.to_bytes(), table_name)

    @staticmethod
    def list_column(table_name: str):
        page_data = BufferManager.load(table_name, 0)
        return MetaPage.from_page(page_data).list_columns()


class MetaPage:

    def __init__(self):
        self.data: bytes = bytes(0)

    @classmethod
    def new_page(cls, columns: List[str]):
        instance = cls()
        instance.data = len(columns).to_bytes(4)
        for col in columns:
            instance.data += col.encode('utf-8').rjust(32, b'\x00')
        instance.data = instance.data.ljust(8 * 1024, b'\x00')
        return instance

    @classmethod
    def from_page(cls, content: bytes):
        instance = cls()
        instance.data = content
        return instance

    def list_columns(self):
        num_columns = int.from_bytes(self.data[:4])
        col_list = []
        for i in range(num_columns):
            byte_start = 4 + i * 32
            byte_end = 4 + (i + 1) * 32
            col_bytes = self.data[byte_start:byte_end]
            col_list.append(col_bytes.decode('utf-8').strip('\x00'))
        return col_list

    def to_bytes(self):
        return self.data

