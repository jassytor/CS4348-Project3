# btree.py
from typing import List
from block import BLOCK_SIZE, pack_u64, unpack_u64

# Minimal degree t = 10 (given in spec).
MIN_DEGREE = 10

# So max keys per node = 2t - 1 = 19, max children = 20.
MAX_KEYS = 2 * MIN_DEGREE - 1  # 19
MAX_CHILDREN = MAX_KEYS + 1    # 20


class BTreeNode:
    """
    One B-tree node stored in a single 512-byte block.

    Layout in the block (matches the spec exactly):

    [0..7]     : block id (where this node lives)
    [8..15]    : parent block id (0 if this is the root)
    [16..23]   : number of key/value pairs currently in this node (0..19)
    [24..(24+152)-1]   : 19 keys (each 8 bytes -> 19 * 8 = 152)
    [next 152 bytes]   : 19 values
    [next 160 bytes]   : 20 child pointers (block ids, 0 if no child)
    [rest of 512]      : unused
    """

    def __init__(
        self,
        block_id: int,
        parent_id: int = 0,
        num_keys: int = 0,
        keys: List[int] | None = None,
        values: List[int] | None = None,
        children: List[int] | None = None,
    ):
        self.block_id = block_id
        self.parent_id = parent_id
        self.num_keys = num_keys

        # Fixed-size arrays so they always serialize to the correct length.
        self.keys: List[int] = [0] * MAX_KEYS if keys is None else list(keys)
        self.values: List[int] = [0] * MAX_KEYS if values is None else list(values)
        self.children: List[int] = [0] * MAX_CHILDREN if children is None else list(children)

        # Make sure arrays are exactly the expected size.
        if len(self.keys) != MAX_KEYS:
            self.keys = (self.keys + [0] * MAX_KEYS)[:MAX_KEYS]
        if len(self.values) != MAX_KEYS:
            self.values = (self.values + [0] * MAX_KEYS)[:MAX_KEYS]
        if len(self.children) != MAX_CHILDREN:
            self.children = (self.children + [0] * MAX_CHILDREN)[:MAX_CHILDREN]

    # ---- Serialization / deserialization ----

    def serialize(self) -> bytes:
        """
        Convert this node into a 512-byte block suitable for writing to disk.
        """
        block = bytearray(BLOCK_SIZE)
        offset = 0

        # Block ID
        block[offset:offset + 8] = pack_u64(self.block_id)
        offset += 8

        # Parent Block ID
        block[offset:offset + 8] = pack_u64(self.parent_id)
        offset += 8

        # Number of keys currently in this node
        block[offset:offset + 8] = pack_u64(self.num_keys)
        offset += 8

        # 19 keys
        for i in range(MAX_KEYS):
            block[offset:offset + 8] = pack_u64(self.keys[i])
            offset += 8

        # 19 values
        for i in range(MAX_KEYS):
            block[offset:offset + 8] = pack_u64(self.values[i])
            offset += 8

        # 20 child pointers (block ids)
        for i in range(MAX_CHILDREN):
            block[offset:offset + 8] = pack_u64(self.children[i])
            offset += 8

        # Remaining bytes stay zero (unused)
        return block

    @classmethod
    def deserialize(cls, data: bytes):
        """
        Create a BTreeNode from a 512-byte block read from disk.
        """
        if len(data) != BLOCK_SIZE:
            raise ValueError("Node block is wrong size")

        offset = 0
        block_id = unpack_u64(data[offset:offset + 8])
        offset += 8

        parent_id = unpack_u64(data[offset:offset + 8])
        offset += 8

        num_keys = unpack_u64(data[offset:offset + 8])
        offset += 8

        keys: List[int] = []
        for _ in range(MAX_KEYS):
            keys.append(unpack_u64(data[offset:offset + 8]))
            offset += 8

        values: List[int] = []
        for _ in range(MAX_KEYS):
            values.append(unpack_u64(data[offset:offset + 8]))
            offset += 8

        children: List[int] = []
        for _ in range(MAX_CHILDREN):
            children.append(unpack_u64(data[offset:offset + 8]))
            offset += 8

        return cls(
            block_id=block_id,
            parent_id=parent_id,
            num_keys=num_keys,
            keys=keys,
            values=values,
            children=children,
        )
