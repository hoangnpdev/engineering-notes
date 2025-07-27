from mini_posgres.buffer_manager import BufferManager
from mini_posgres.config import Config

class FSM:
    """
    each byte of FSM page is corresponding to a TuplePage (256 unit). 1 unit = round_down(block_size / 256 - 32 byte)

    structure:
    root:
        branch#1:
            leaf#1
            leaf#4096
        branch#4096:
            leaf#1:
            leaf#4096:
    use table's current num of row to determine if a node is unassigned or it's tuple page is empty.
    """
    def __init__(self, table_name):
        self.table_name = table_name


    def get_l2_block_position(self, l1_leaf_position):
        # todo
        return 0

    def get_l3_block_position(self, l1_leaf_position, l2_leaf_position):
        # todo
        return 0

    def get_tuple_block_position(self, l1_leaf_position, l2_leaf_position, l3_leaf_position):
        # todo
        return 0

    def find_block_with_enough_free_space(self, minimal_free_space, num_current_blocks=0):
        # root traverse (l1)
        block_0 = BufferManager.load_fsm_block(self.table_name, 0)
        l1_leaf_position = FSMBlock.from_block(block_0).traverse(minimal_free_space)
        # l2 traverse
        BufferManager.load_fsm_block(self.table_name, 0)
        l2_block_position = self.get_l2_block_position(l1_leaf_position)
        l2_block = BufferManager.load_fsm_block(self.table_name, l2_block_position)
        l2_leaf_position = FSMBlock.from_block(l2_block).traverse(minimal_free_space)
        # l3 traverse
        l3_block_position = self.get_l3_block_position(l1_leaf_position, l2_leaf_position)
        l3_block = BufferManager.load_fsm_block(self.table_name, l3_block_position)
        l3_leaf_position = FSMBlock.from_block(l3_block).traverse(minimal_free_space)
        return self.get_tuple_block_position(l1_leaf_position, l2_leaf_position, l3_leaf_position)

    def update_block_free_space_left(self, block_offset, new_free_size):
        return  # todo


# only handle fsm block
class FSMBlock:
    def __init__(self):
        self.data = bytes(0)

    @classmethod
    def new_root_block(cls):
        instance = cls()
        instance.data.ljust(Config.PAGE_SIZE, b'\x00')
        return instance

    @classmethod
    def from_block(cls, block: bytes):
        instance = cls()
        instance.data = block
        return instance

    def traverse(self, minimal_free_space, num_of_active_leaf):
        # todo
        # 1 fsm block's tree depth 12 + 1 level: 0 -> 12

        if self.data[1] < minimal_free_space:
            return -1
        node_pos_in_last_level = 1
        for level in range(0, 12 + 1):
            left_child_pos = 2 * (node_pos_in_last_level - 1) + 1
            left_child = 2 ** level + left_child_pos
            if self.data[left_child] > minimal_free_space:
                node_pos_in_last_level = left_child_pos
                if level == 12:
                    return left_child_pos
                continue
            right_child_pos = 2 * (node_pos_in_last_level - 1) + 2
            right_child = 2 ** level + right_child_pos
            if self.data[right_child] > minimal_free_space:
                node_pos_in_last_level = right_child_pos
                if level == 12:
                    return right_child_pos
                continue
            return -1
    # todo refactor this function

    def to_bytes(self):
        return self.data

