from pathlib import Path
from typing import Final

IN_DIR: Final[Path] = Path(__file__).parent.parent/ "Dataset"
OUT_DIR: Final[Path] = Path(__file__).parent.parent / "results"

assert IN_DIR.exists(), f"inputs directory does not exist: {IN_DIR}"
OUT_DIR.mkdir(exist_ok=True)
