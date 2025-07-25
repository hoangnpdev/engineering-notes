from typing import List, Dict, Any

from mini_posgres.buffer_manager import BufferManager
from mini_posgres.postgres_fsm import FSMBlock
from mini_posgres.postgres_tuple import MetaPage
from mini_posgres.postgres_file import FileManager


# handle table crud operator, no byte operator
class Table:
    def __init__(self, table_name):
        self.table_name: str = table_name

    @classmethod
    def new_table(cls, table_name, columns):
        first_page = MetaPage.new_page(columns)
        fsm_root_block = FSMBlock.new_root_block()
        FileManager.save_table(first_page.to_bytes(), fsm_root_block.to_bytes(), table_name)

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


