from typing import List
from mini_posgres.postgres_io import FileManager
from mini_posgres.buffer_manager import BufferManager
from mini_posgres.page_manager import MetaPage


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

    def insert_row(self):
        # Free Space map


    def update_row(self):
        # = delte old row and insert new row


