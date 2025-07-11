from typing import List, Dict, Any

from mini_posgres.buffer_manager import BufferManager
from mini_posgres.page_manager import MetaPage
from mini_posgres.file_manager import FileManager


class Table:
    def __init__(self, table_name):
        self.table_name: str = table_name

    def columns(self):
        page_data = BufferManager.load(self.table_name, 0)
        return MetaPage.from_page(page_data).list_columns()

    def insert(self, rows: List[Dict[str, Any]]):
        # Free Space map
        return

    def rows(self) -> List[Dict[str, Any]]:
        num_page = FileManager.get_num_pages(self.table_name)
        for i in range(1, num_page):
            page_data = BufferManager.load(self.table_name, i)
        return [{}]

