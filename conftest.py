import sys
from pathlib import Path

# Repository root on sys.path (audit F-07: parents[1] previously
# resolved to the PARENT of the repository).
sys.path.insert(0, str(Path(__file__).resolve().parent))
