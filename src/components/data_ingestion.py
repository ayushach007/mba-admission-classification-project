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
    '''
    Class to ingest data from a source and save it to a destination
    '''
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self) -> pd.DataFrame:
        '''
        This function reads data from MySQL database, saves raw data to raw data directory, splits data into train and test data, and saves train and test data to train and test data directories
        
        Returns:
            - train_data_path: Path to train data
            - test_data_path: Path to test data

        Raises:
            - CustomException: If any error occurs while reading and saving data
        '''
        try:
            data = read_sql_data()  # replace this with read_csv or read_excel if you are reading from a csv or excel file

            data.to_csv(self.config.raw_data_path, index=False, header=True)
            logging.info(f"Raw has been saved successfully at {self.config.raw_data_path}")

            logging.info("Splitting data into train and test data")
            train, test = train_test_split(data, test_size=0.3, random_state=42, stratify=data['admission'])

            logging.info("Data has been split successfully")
            logging.info(f"Train data value counts: {train['admission'].value_counts()}")
            logging.info(f"Test data value counts: {test['admission'].value_counts()}")

            train.to_csv(self.config.train_data_path, index=False, header=True)
            logging.info(f"Train data has been saved successfully at {self.config.train_data_path}")

            test.to_csv(self.config.test_data_path, index=False, header=True)
            logging.info(f"Test data has been saved successfully at {self.config.test_data_path}")
            
            return (
                self.config.train_data_path,
                self.config.test_data_path
            )
        
        except Exception as e:
            raise CustomException(e, sys)