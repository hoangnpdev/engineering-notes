from postgres_io.postgres_io import FileManager


class BufferManager:
    dict = {}

    @classmethod
    def load(cls, table_name, page_offset=0):
        cache_id = f'{table_name}#{str(page_offset)}'
        if cache_id in cls.dict:
            return cls.dict[cache_id]
        page_data = FileManager.read_page(table_name, page_offset)
        cls.dict[cache_id] = page_data
        return page_data


