import os
import shutil
from mini_posgres.config import Config


class FileManager:
    PATH = 'tmp'

    @classmethod
    def save_table(cls, tuple_content: bytes, fsm_content, table_name: str):
        os.mkdir(cls.PATH)
        with open(cls.get_path(table_name), 'wb') as table_file:
            table_file.write(tuple_content)
        with open(cls.get_fsm_path(table_name), 'wb') as fsm_file:
            fsm_file.write(fsm_content)

    @classmethod
    def read_page(cls, filename: str, page_offset=0):
        with open(cls.get_path(filename)) as table_file:
            table_file.seek(page_offset)
            return table_file.read(Config.PAGE_SIZE)

    @classmethod
    def get_num_pages(cls, table_name: str):
        return cls.get_table_size(table_name) / Config.PAGE_SIZE

    @classmethod
    def get_table_size(cls, filename: str):
        return os.path.getsize(cls.get_path(filename))

    @classmethod
    def destroy(cls):
        shutil.rmtree(cls.PATH)

    @classmethod
    def get_path(cls, table_name: str):
        return f'{cls.PATH}/{table_name}.tbl'

    @classmethod
    def get_fsm_path(cls, table_name: str):
        return f'{cls.PATH}/{table_name}.fsm'






