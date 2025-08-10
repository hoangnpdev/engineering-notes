from mini_cross.postgres.postgres_file import FileManager


class BufferManager:
    dict = {}
    fsm_dict = {}

    @classmethod
    def load(cls, table_name, page_offset=0):
        cache_id = f'{table_name}#{str(page_offset)}'
        if cache_id in cls.dict:
            return cls.dict[cache_id]
        page_data = FileManager.read_tuple_block(table_name, page_offset)
        cls.dict[cache_id] = page_data
        return page_data

    @classmethod
    def load_fsm_block(cls, table_name, block_offset=0):
        cache_id = f'{table_name}#{block_offset}'
        if cache_id in cls.fsm_dict:
            return cls.fsm_dict[cache_id]
        fsm_block = FileManager.read_fsm_block(table_name, block_offset)
        cls.fsm_dict[cache_id] = fsm_block
        return fsm_block

