import os
import shutil
from dataclasses import dataclass


class FileManager:
    PATH = 'tmp'

    @classmethod
    def save_table(cls, content: bytes, filename: str):
        os.mkdir(cls.PATH)
        with open(cls.get_path(filename), 'wb') as table_file:
            table_file.write(content)

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
    def get_path(cls, filename: str):
        return f'{cls.PATH}/{filename}.tbl'



@dataclass(frozen=True)
class Config:
    PAGE_SIZE = 8 * 1024



