import sys
from src.logger import logging
from src.exception import CustomException
from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation

class DataTransformationPipeline:
    def __init__(self):
        logging.info("Data Transformation Pipeline initiated")

    def main(self):
        try:
            # initialize configuration manager
            config_manager = ConfigurationManager()

            # Data Ingestion
            obj = DataIngestion()
            train_data, test_data = obj.initiate_data_ingestion()

            # Data Transformation
            data_transformation_config = config_manager.get_data_transformation_config()
            data_transformation = DataTransformation(data_transformation_config)
            data_transformation.initiate_data_transformation(train_data, test_data)

        except Exception as e:
            raise CustomException(e, sys)
        
STAGE_NAME = "Data Transformation"

if __name__ == "__main__":
    try:
        logging.info(f"Starting {STAGE_NAME} Pipeline")
        data_ingestion_pipeline = DataTransformationPipeline()
        data_ingestion_pipeline.main()
        logging.info(f"Completed {STAGE_NAME} Pipeline")

    except CustomException as e:
        raise CustomException(e, sys)