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
    def __init__(self):
        self.data: bytes = bytes(0)


    def traverse_fsm_block(self, fsm_block_position, minimal_free_space):
        # todo
        return 0

    def get_l2_block_position(self, l1_leaf_position):
        # todo
        return 0

    def get_l3_block_position(self, l1_leaf_position, l2_leaf_position):
        # todo
        return 0

    def get_tuple_block_position(self, l1_leaf_position, l2_leaf_position, l3_leaf_position):
        # todo
        return 0

    def find_block_with_enough_free_space(self, minimal_free_space):
        l1_leaf_position = self.traverse_fsm_block(0, minimal_free_space)
        l2_block_position = self.get_l2_block_position(l1_leaf_position)
        l2_leaf_position = self.traverse_fsm_block(l2_block_position, minimal_free_space)
        l3_block_position = self.get_l3_block_position(l1_leaf_position, l2_leaf_position)
        l3_leaf_position = self.traverse_fsm_block(l3_block_position, minimal_free_space)
        return self.get_tuple_block_position(l1_leaf_position, l2_leaf_position, l3_leaf_position)


class FSMPage:
    def __init__(self):
        self.data = bytes(0)

