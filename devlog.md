## 2025-12-10 4:34PM

Thoughts:
This session was focused on setting up the project environment. No new design changes yet.

Plan:
Initialized the Git repository, created the required project files, and set up the basic folder structure. The goal was to get everything ready so development can start cleanly in the next session.

## 2025-12-10 5:12PM

Thoughts:
Today I set up the basic file layout for the disk-based B-tree index. I focused on matching the exact block formats from the project handout.

Plan:
- Implemented block.py with the 512-byte header block, magic number, root id, and next block id using 8-byte big-endian integers.
- Implemented btree.py with a BTreeNode class that serializes/deserializes nodes with 19 keys, 19 values, and 20 child pointers.
- Wrote main.py so the 'create' command makes a new valid index file with an empty tree.
Next session I plan to start on the 'insert' command and make sure I never keep more than three nodes in memory at once.
