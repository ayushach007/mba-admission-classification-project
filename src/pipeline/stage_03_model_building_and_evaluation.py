import sys
from src.logger import logging
from src.exception import CustomException
from src.config.configuration import ConfigurationManager
from src.components.model_building_and_evaluation import ModelBuilding
from src.pipeline.stage_02_data_transformation_pipeline import DataTransformationPipeline
import warnings
warnings.filterwarnings("ignore")


class ModelBuildingPipeline:
    '''
    This class is responsible for initiating the Model Building Pipeline
    '''
    def __init__(self, train_array, test_arr):
        self.train_array = train_array
        self.test_arr = test_arr
        logging.info("Model Building Pipeline initiated")

    def main(self):
        '''
        This function initiates the Model Building Pipeline
        
        Raises:
            - CustomException: If any error occurs while initiating the Model Building Pipeline
        '''
        try:
            config = ConfigurationManager()
            model_training_config = config.get_model_config()
            model_building = ModelBuilding(model_training_config)
            model_building.initiate_model_building(train_arr=self.train_array, test_arr=self.test_arr)

        except Exception as e:
            raise CustomException(e, sys)
        
