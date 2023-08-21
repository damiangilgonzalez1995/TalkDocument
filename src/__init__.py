import utils.util
import os
import sys

# Add the path of this building block to sys.path
root_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)