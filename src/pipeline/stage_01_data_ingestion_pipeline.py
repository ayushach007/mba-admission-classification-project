import sys
from src.logger import logging
from src.exception import CustomException
from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
import warnings
warnings.filterwarnings("ignore")

class DataIngestionPipeline:
    '''
    This class is responsible for initiating the Data Ingestion Pipeline
    '''
    def __init__(self):
        logging.info("Data Ingestion Pipeline initiated")

    def main(self):
        '''
        This function initiates the Data Ingestion Pipeline

        Returns:
            - training_data: Training data
            - testing_data: Testing data

        Raises:
            - CustomException: If any error occurs while initiating the Data Ingestion Pipeline
        '''
        try:
            config_manager = ConfigurationManager()
            data_ingestion_config = config_manager.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)
            training_data, testing_data = data_ingestion.initiate_data_ingestion()

            return training_data, testing_data
        except Exception as e:
            raise CustomException(e, sys)
        