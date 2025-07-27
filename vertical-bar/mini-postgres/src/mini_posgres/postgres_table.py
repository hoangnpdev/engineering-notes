from typing import List, Dict, Any

from mini_posgres.buffer_manager import BufferManager
from mini_posgres.postgres_fsm import FSMBlock, FSM
from mini_posgres.postgres_tuple import MetaPage, TuplePage, Tuple
from mini_posgres.postgres_file import FileManager


# handle table crud operator, no byte operator
class Table:
    def __init__(self, table_name):
        self.table_name: str = table_name
        self.fsm: FSM = FSM(table_name)

    @classmethod
    def new_table(cls, table_name, columns):
        first_page = MetaPage.new_page(columns)
        fsm_root_block = FSMBlock.new_root_block()
        FileManager.save_table(first_page.to_bytes(), fsm_root_block.to_bytes(), table_name)

    def columns(self):
        page_data = BufferManager.load(self.table_name, 0)
        return MetaPage.from_page(page_data).list_columns()

    def insert(self, rows: List[Dict[str, Any]]):
        for row in rows:
            # calculate tuple size
            i_tuple = Tuple(row)
            block_offset = self.fsm.find_block_with_enough_free_space(
                i_tuple.tuple_size(),
                self.size()
            )
            block_data = BufferManager.load_fsm_block(self.table_name, block_offset)
            block = TuplePage.from_page(block_data)
            block.insert_tuple(i_tuple)
            # update fsm
            self.fsm.update_block_free_space_left(block_offset, block.free_space_left())

    def rows(self) -> List[Dict[str, Any]]:
        num_page = FileManager.get_num_pages(self.table_name)
        for i in range(1, num_page):
            page_data = BufferManager.load(self.table_name, i)
        return [{}]

    def size(self):
        return FileManager.get_num_pages(self.table_name)


