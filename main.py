# main.py
import os
import sys

from block import write_header
from block import BLOCK_SIZE
from btree import BTreeNode


def cmd_create(index_filename: str) -> None:
    """
    Handle:  project3 create <indexfile>

    - If the file already exists, print an error and exit.
    - Otherwise, create a new empty index file:
        * Block 0 = header (magic, root id = 0, next block id = 1)
        * No nodes yet (tree is empty).
    """
    if os.path.exists(index_filename):
        print(f"error: index file '{index_filename}' already exists")
        sys.exit(1)

    # Create and initialize the file.
    with open(index_filename, "wb+") as f:
        root_block_id = 0  # tree is empty at creation time
        next_block_id = 1  # first node we allocate later will use block 1

        # Write header to block 0
        write_header(f, root_block_id=root_block_id, next_block_id=next_block_id)

        # No node blocks yet; we only allocate them when we insert.

    print(f"created empty index file '{index_filename}'")


def main() -> None:
    # Expect at least: python3 main.py <command> ...
    if len(sys.argv) < 3:
        print("usage: python3 main.py <command> <indexfile> [args...]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "create":
        index_filename = sys.argv[2]
        cmd_create(index_filename)
    else:
        # For now we only implement 'create'.
        # We'll add: insert, search, load, print, extract later.
        print(f"error: command '{command}' is not implemented yet")
        sys.exit(1)


if __name__ == "__main__":
    main()
