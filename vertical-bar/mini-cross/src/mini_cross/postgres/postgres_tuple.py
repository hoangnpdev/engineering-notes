from typing import List, Dict, Any


class MetaPage:
    """
        4 bytes: num of column.
        arr of 32 bytes: each is column name.
    """
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


class Tuple:
    """
    array of bytes: all field is serialized sequentially
    """
    def __init__(self, row: Dict[str, Any]):
        self.data: bytes = bytes[0]  # todo

    def tuple_size(self):
        return 0  # todo


class TuplePage:
    """
    arr of 4 bytes: each entry is an (offset, length) pointing to actual tuple
    ...
    arr of tuples/rows: is stored in reversed order from bottom of page.
    """
    def __init__(self):
        self.data: bytes = bytes(0)

    @classmethod
    def from_page(cls, content: bytes):
        instance = cls()
        instance.data = content
        return instance

    def free_space_left(self):
        return  # todo

    def insert_tuple(self, tuple: Tuple):
        return  # todo

    def rows(self):
        return []



