from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Table(ABC):

    @abstractmethod
    def columns(self):
        pass

    @abstractmethod
    def insert(self, rows: List[Dict[str, Any]]):
        pass

    @abstractmethod
    def rows(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def size(self):
        pass


class TableRef:

    def __init__(self, table: Table):
        self.table = table

    # for simplicity, this function only have count logic
    def hash_aggregate(self, group_key: List[str]) -> List[Dict[str, Any]]:
        # todo
        pass





