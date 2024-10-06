import sys
from src.logger import logging
from src.exception import CustomException
from src import *
from src.utils.common import read_yaml_file, create_directory
from src.entity.config_entity import (DataIngestionConfig, DataTransformationConfig, ModelTrainingConfig)

class ConfigurationManager:
    '''
    Class to manage configuration and parameters files
    '''
    def __init__(self,config_file_path = CONFIG_FILE_PATH):
        '''
        This function reads configuration and parameters files, creates directories to store artifacts
        '''
        try:
            self.config = read_yaml_file(config_file_path)

            logging.info("Configuration and Parameters files have been read successfully")

            create_directory([self.config.artifacts_directory])
            logging.info("Artifacts directory has been created successfully")
        except Exception as e:
            raise CustomException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        '''
        This function gets data ingestion configuration, creates root directory to store raw data, train data and test data, assigns paths to raw data, train data and test data, and returns data ingestion configuration

        Returns:
            - data_ingestion_config: DataIngestionConfig object
        '''
        try:
            config = self.config.data_ingestion

            create_directory([config.root_dir])

            logging.info("DataIngestion directory has been created successfully to store raw data, train data and test data")

            data_ingestion_config = DataIngestionConfig(
                raw_data_path = config.raw_data_path,
                train_data_path = config.train_data_path,
                test_data_path = config.test_data_path
            )

            logging.info("Paths have been assigned successfully to raw data, train data and test data")

            logging.info("Returning data ingestion config")

            return data_ingestion_config
        
        except Exception as e:
            raise CustomException(e, sys)
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        '''
        This function gets data transformation configuration, creates root directory to store transformed data, assigns paths to preprocessor object, train array and test array, and returns data transformation configuration
        
        Returns:
            - data_transformation_config: DataTransformationConfig object
        '''
        try:
            config = self.config.data_transformation

            create_directory([config.root_dir])

            logging.info("DataTransformation directory have been created successfully to store transformed data")

            data_transformation_config = DataTransformationConfig(
                preprocessor_obj_path = config.preprocessor_obj_path,
                train_arr = config.train_arr_path,
                test_arr = config.test_arr_path
            )

            logging.info("Paths have been assigned successfully to preprocessor object, train array and test array")

            logging.info("Returning data transformation config")
            return data_transformation_config

        except Exception as e:
            raise CustomException(e, sys)
    
    def get_model_config(self) -> ModelTrainingConfig:
        '''
        This function gets model training configuration, creates root directory to store model artifacts, assigns paths to model and model metrics, and returns model training configuration

        Returns:
            - model_config: ModelTrainingConfig object
        '''
        try:
            config = self.config.model_training

            create_directory([config.root_dir])

            logging.info("Model directory has been created successfully to store model artifacts")

            model_config = ModelTrainingConfig(
                model_path = config.model_path,
                training_metrics = config.training_metrics,
                test_metrics = config.test_metrics,
                )
            
            logging.info("Paths have been assigned successfully to model and model metrics")

            return model_config
        
        except Exception as e:
            raise CustomException(e, sys)

    
        