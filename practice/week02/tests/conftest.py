import sys
from pathlib import Path

WEEK02 = Path(__file__).resolve().parents[1]
if str(WEEK02) not in sys.path:
    sys.path.insert(0, str(WEEK02))
