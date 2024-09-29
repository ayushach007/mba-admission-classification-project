from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    raw_data_path: Path
    train_data_path: Path
    test_data_path: Path

@dataclass(frozen=True)
class DataTransformationConfig:
    preprocessor_obj_path: Path
    train_arr: Path
    test_arr: Path

@dataclass(frozen=True)
class ModelTrainingConfig:
    model_path: Path
    model_metrics_path: Path