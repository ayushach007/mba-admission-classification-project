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
        
STAGE_NAME = "Data Transformation"

if __name__ == "__main__":
    try:

        logging.info(f"Starting {STAGE_NAME} Pipeline")

        logging.info('Reading data from previous stage: Data Ingestion')
        # Instantiate DataIngestionPipeline to get training and testing data
        data_ingestion_pipeline = DataIngestionPipeline()
        training_data, testing_data = data_ingestion_pipeline.main()

        logging.info('Data read successfully from previous stage: Data Ingestion')

        # Pass the data to DataTransformationPipeline
        data_transformation_pipeline = DataTransformationPipeline(training_data, testing_data)
        train_arr, test_arr = data_transformation_pipeline.main()

        logging.info(f"Completed {STAGE_NAME}  successfully.")
    except CustomException as e:
        logging.error(f"Error in {STAGE_NAME}: {e}")
        raise CustomException(e, sys)