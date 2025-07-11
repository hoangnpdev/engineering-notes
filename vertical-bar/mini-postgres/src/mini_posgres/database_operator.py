from typing import List
from mini_posgres.file_manager import FileManager
from mini_posgres.buffer_manager import BufferManager
from mini_posgres.table_operator import Table
from mini_posgres.page_manager import MetaPage


class MiniPostgres:

    @staticmethod
    def create_table(table_name, columns: List[str]):
        # convert column_name to bytes
        first_page = MetaPage.new_page(columns)
        FileManager.save_table(first_page.to_bytes(), table_name)

    @staticmethod
    def load_table(table_name: str) -> Table:
        return Table(table_name)



