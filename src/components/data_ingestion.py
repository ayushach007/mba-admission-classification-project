import pandas as pd
import sys
from src.logger import logging
from src.exception import CustomException
from src.utils.common import read_sql_data
from src.entity.config_entity import DataIngestionConfig, DataTransformationConfig
from src.components.data_transformation import DataTransformation
from src.components.model_building_and_evaluation import ModelTrainingConfig, ModelBuilding
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self) -> pd.DataFrame:
        try:
            logging.info("Reading data from MySQL database")
            data = read_sql_data()
            logging.info("Data has been read successfully")

            logging.info("Saving data to raw data directory")
            data.to_csv(self.config.raw_data_path, index=False, header=True)
            logging.info(f"Raw has been saved successfully at {self.config.raw_data_path}")

            logging.info("Splitting data into train and test data")
            train, test = train_test_split(data, test_size=0.3, random_state=42)
            logging.info("Data has been split successfully")

            logging.info("Saving train data to train data directory")
            train.to_csv(self.config.train_data_path, index=False, header=True)
            logging.info(f"Train data has been saved successfully at {self.config.train_data_path}")

            logging.info("Saving test data to test data directory")
            test.to_csv(self.config.test_data_path, index=False, header=True)
            logging.info(f"Test data has been saved successfully at {self.config.test_data_path}")
            
            return (
                self.config.train_data_path,
                self.config.test_data_path
            )
        
        except Exception as e:
            raise CustomException(e, sys)