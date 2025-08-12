

class IBlock:
    def __init__(self):
        pass


class IColumn:
    def __init__(self):
        pass

class MetaBlock:
    def __init__(self, columns, keys):
        pass

    def to_bytes(self):
        pass
