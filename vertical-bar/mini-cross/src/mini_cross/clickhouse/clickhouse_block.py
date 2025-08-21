

class IPart:

    def __init__(self, part_name):
        pass

    @classmethod
    def new_part(cls):
        part_name = None # Logic to generate a new part name
        return cls(part_name)


class IBlock:
    def __init__(self):
        pass


class IColumn:
    def __init__(self):
        pass

class MetaBlock:
    def __init__(self):
        pass

    def to_bytes(self):
        pass

    @classmethod
    def from_bytes(cls, data):
        pass

    @classmethod
    def new(cls, columns, keys):
        return cls()

