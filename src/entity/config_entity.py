from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    raw_data_path: Path
    train_data_path: Path
    test_data_path: Path