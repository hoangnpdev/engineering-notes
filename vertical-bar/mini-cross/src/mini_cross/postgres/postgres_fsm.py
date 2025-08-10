from mini_cross.postgres.buffer_manager import BufferManager
from mini_cross.postgres.config import Config

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
    for simplicity, I just implement one level block.
    use table's current num of row to determine if a node is unassigned, or it's tuple page is empty.
    """
    def __init__(self, table_name):
        self.table_name = table_name

    def find_block_with_enough_free_space(self, minimal_free_space, num_current_blocks=0):
        block = BufferManager.load_fsm_block(self.table_name, 0)
        leaf_position = FSMBlock.from_block(block).traverse(minimal_free_space, num_current_blocks)
        return leaf_position

    def update_tuple_block_free_space_size(self, tuple_block_offset, new_free_space_size):
        block = BufferManager.load_fsm_block(self.table_name, 0)
        FSMBlock.from_block(block).update_leaf_value(tuple_block_offset, new_free_space_size)


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
        # 1 fsm block's tree depth 1 + 12 level: 0 -> 12
        if self.data[1] < minimal_free_space:
            return -1
        node_pos = 1
        while self.get_level(node_pos) <= 12:
            if self.get_level(node_pos) == 12:
                return self.get_leaf_pos(node_pos)
            left_node_pos = self.get_left_child_pos(node_pos)
            if (self.data[left_node_pos] >= minimal_free_space
                    and not self.is_out_of_bounds(node_pos, num_of_active_leaf)):
                node_pos = left_node_pos

                continue
            right_node_pos = self.get_right_child_pos(node_pos)
            if (self.data[right_node_pos] >= minimal_free_space
                    and not self.is_out_of_bounds(node_pos, num_of_active_leaf)):
                node_pos = right_node_pos
                continue
            return -1

    def update_leaf_value(self, leaf_offset, new_leaf_value):
        block = bytearray(self.data)
        node_pos = 2 ** 12 + leaf_offset
        block[new_leaf_value] = new_leaf_value
        while self.get_level(node_pos) >= 0:
            parent_pos = self.get_parent_pos(node_pos)
            left_child_pos = self.get_left_child_pos(parent_pos)
            right_child_pos = self.get_right_child_pos(parent_pos)
            old_parent_value = block[parent_pos]
            block[parent_pos] = max(block[left_child_pos], block[right_child_pos])
            if old_parent_value == block[parent_pos]:
                break
        self.data = bytes(block)

    def is_out_of_bounds(self, node_pos, num_of_active_leaf):
        node_level = self.get_level(node_pos)
        level_boundary = num_of_active_leaf
        for level in range(12, node_level - 1, -1):
            level_boundary = level_boundary / 2 + level_boundary % 2
        node_pos_in_row = self.get_node_pos_in_row(node_pos)
        return node_pos_in_row > level_boundary

    def get_parent_pos(self, child_pos):
        # todo
        return 0

    def get_left_child_pos(self, parent_pos):
        # todo
        return 0

    def get_right_child_pos(self, parent_pos):
        # todo
        return 0

    def get_level(self, node_pos):
        # todo
        return 12

    # 1 -> ...
    def get_node_pos_in_row(self, node_pos):
        # todo
        return 0

    # 1 -> ...
    def get_leaf_pos(self, node_pos):
        # todo
        return 0

    def to_bytes(self):
        return self.data

