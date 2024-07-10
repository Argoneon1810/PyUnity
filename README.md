# PyUnity
Bare bone TCP communication between Python and Unity.

# Versions
- Unity 2021.3.3f
- Python 3.10.11
- no other external dependency

# Branch info
This branch is intended to suggest an alternative solution for communication size, where buffer size is not fixed by default size, which is 1024 bytes, but rather match the size of the actual data.

This may be useful if there are cases where the data size is larger than 1024 bytes, or too small that most of the time, buffer dimensions are being waisted.

However, this change requires twice the number of network transaction. This may be impractical in some cases where the network is very vulnerable.

Therefore it is not merged into main branch, but pushed into separate one.
