from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    '''
    This class holds the configuration for data ingestion
    '''
    raw_data_path: Path
    train_data_path: Path
    test_data_path: Path

@dataclass(frozen=True)
class DataTransformationConfig:
    '''
    This class holds the configuration for data transformation
    '''
    preprocessor_obj_path: Path
    train_arr: Path
    test_arr: Path

@dataclass(frozen=True)
class ModelTrainingConfig:
    '''
    This class holds the configuration for model training
    '''
    model_path: Path
    training_metrics: Path
    test_metrics: Path