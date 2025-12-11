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

## 2025-12-10 10:27 PM

Thoughts:
I tested the `create` command today to make sure the index file was being built correctly. Running the command created a new file with exactly one 512-byte header block, and the header values matched what the project specifies. It helped confirm that the magic string, root ID, and next block ID are all being written in the right places.

Plan:
Next step is starting the insert logic. Before that, I want to finalize how nodes will be read/written from disk and make sure the project stays within the rule of keeping at most three nodes in memory at once. After that I can move into implementing the first simple insert (no split), then splitting internal and leaf nodes.
