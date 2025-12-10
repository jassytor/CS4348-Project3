# block.py
import struct

# Each block in the index file is exactly 512 bytes.
BLOCK_SIZE = 512

# All numbers in the file are 8-byte integers (unsigned) in big-endian order.
INT_SIZE = 8

# Magic number from the project spec ("4348PRJ3" as ASCII bytes).
MAGIC = b"4348PRJ3"


def pack_u64(value: int) -> bytes:
    """
    Pack an integer into 8 bytes (unsigned, big-endian).
    """
    return value.to_bytes(INT_SIZE, byteorder="big", signed=False)


def unpack_u64(data: bytes) -> int:
    """
    Unpack an 8-byte (unsigned, big-endian) integer.
    """
    return int.from_bytes(data, byteorder="big", signed=False)


def write_header(f, root_block_id: int, next_block_id: int) -> None:
    """
    Write the 512-byte header block (block 0):

    [0..7]   : "4348PRJ3"
    [8..15]  : root block id (0 if tree is empty)
    [16..23] : next block id to allocate
    [24..511]: unused (left as zeros)
    """
    block = bytearray(BLOCK_SIZE)

    # Magic string
    block[0:8] = MAGIC

    # Root ID
    block[8:16] = pack_u64(root_block_id)

    # Next Block ID
    block[16:24] = pack_u64(next_block_id)

    # Remaining bytes are already zero-filled
    f.seek(0)
    f.write(block)


def read_header(f):
    """
    Read and validate the header block. Returns (root_block_id, next_block_id).
    Raises ValueError if the magic number is wrong or header is invalid.
    """
    f.seek(0)
    data = f.read(BLOCK_SIZE)
    if len(data) != BLOCK_SIZE:
        raise ValueError("Invalid index file: header too short")

    if data[0:8] != MAGIC:
        raise ValueError("Invalid index file: bad magic number")

    root_block_id = unpack_u64(data[8:16])
    next_block_id = unpack_u64(data[16:24])
    return root_block_id, next_block_id
