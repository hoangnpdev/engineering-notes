from mini_posgres.postgres_file import FileManager


class BufferManager:
    dict = {}
    fsm_dict = {}

    @classmethod
    def load(cls, table_name, page_offset=0):
        cache_id = f'{table_name}#{str(page_offset)}'
        if cache_id in cls.dict:
            return cls.dict[cache_id]
        page_data = FileManager.read_page(table_name, page_offset)
        cls.dict[cache_id] = page_data
        return page_data

    @classmethod
    def load_fsm_block(cls, table_name, block_offset=0):
        # todo
        return None

