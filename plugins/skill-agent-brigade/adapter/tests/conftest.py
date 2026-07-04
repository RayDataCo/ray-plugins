import sys
from pathlib import Path

# adapter/tests/conftest.py -> parent.parent is adapter/, where rail_adapter.py
# lives. Inserted explicitly so `import rail_adapter` works regardless of the
# directory pytest is invoked from (repo root, per the task's run command).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
