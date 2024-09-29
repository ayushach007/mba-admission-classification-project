import sys
from src.logger import logging
from src.exception import CustomException
from src import *
from src.utils.common import read_yaml_file, create_directory
from src.entity.config_entity import DataIngestionConfig

class ConfigurationManager:
    def __init__(self,
                  config_file_path = CONFIG_FILE_PATH,
                  params_file_path = PARAMS_FILE_PATH):
        try:
            self.config = read_yaml_file(config_file_path)

            logging.info("Configuration and Parameters files have been read successfully")

            logging.info("Creating directories to store artifacts")
            create_directory([self.config.artifacts_directory])
            logging.info("Directories have been created successfully")
        except Exception as e:
            raise CustomException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            config = self.config.data_ingestion

            logging.info("Creating root directory to store raw data, train data and test data")

            create_directory([config.root_dir])

            logging.info("Root directory has been created successfully")

            logging.info("Assigning paths to raw data, train data and test data")

            data_ingestion_config = DataIngestionConfig(
                raw_data_path = config.raw_data_path,
                train_data_path = config.train_data_path,
                test_data_path = config.test_data_path
            )

            logging.info("Paths have been assigned successfully")

            return data_ingestion_config
        
        except Exception as e:
            raise CustomException(e, sys)
    
        