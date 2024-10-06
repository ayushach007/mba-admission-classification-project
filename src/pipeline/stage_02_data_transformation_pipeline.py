import sys
from src.logger import logging
from src.exception import CustomException
from src.config.configuration import ConfigurationManager
from src.pipeline.stage_01_data_ingestion_pipeline import DataIngestionPipeline
from src.components.data_transformation import DataTransformation

import warnings
warnings.filterwarnings("ignore")

class DataTransformationPipeline(DataIngestionPipeline):
    '''
    This class is responsible for initiating the Data Transformation Pipeline
    '''
    def __init__(self, training_data, testing_data):
        self.training_data = training_data
        self.testing_data = testing_data

        logging.info("Data Transformation Pipeline initiated")

    def main(self):
        '''
        This function initiates the Data Transformation Pipeline
        
        Returns:
            - train_arr: Transformed training data
            - test_arr: Transformed testing data
            
        Raises:
            - CustomException: If any error occurs while initiating the Data Transformation Pipeline
        '''
        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            data_transformation = DataTransformation(data_transformation_config)
            train_arr, test_arr, _ = data_transformation.initiate_data_transformation(training_data=self.training_data, testing_data=self.testing_data)

            return train_arr, test_arr
            
        except Exception as e:
            raise CustomException(e, sys)
        