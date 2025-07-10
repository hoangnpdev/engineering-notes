import shutil, os
from dataclasses import dataclass


class FileManager:
    PATH = 'tmp'

    @classmethod
    def save_table(cls, content: bytes, filename: str):
        os.mkdir(cls.PATH)
        with open(f'{cls.PATH}/{filename}.tbl', 'wb') as table_file:
            table_file.write(content)

    @classmethod
    def read_page(cls, filename: str, page_offset=0):
        with open(f'{cls.PATH}/{filename}.tbl', 'rb') as table_file:
            table_file.seek(page_offset)
            return table_file.read(Config.PAGE_SIZE)

    @classmethod
    def destroy(cls):
        shutil.rmtree(cls.PATH)


@dataclass(frozen=True)
class Config:
    PAGE_SIZE = 8 * 1024



