import sys
from src.logger import logging
from src.exception import CustomException
from src.config.configuration import ConfigurationManager
from src.components.model_building_and_evaluation import ModelBuilding

class ModelBuildingPipeline:
    def __init__(self):
        logging.info("Model Building Pipeline initiated")

    def main(self):
        try:
            config = ConfigurationManager()
            model_training_config = config.get_model_config()
            model_building = ModelBuilding(model_training_config)
            model_building.initiate_model_building()

        except Exception as e:
            raise CustomException(e, sys)
        
STAGE_NAME = "Model Building"

if __name__ == "__main__":
    try:
        logging.info(f"Starting {STAGE_NAME} Pipeline")
        model_building_pipeline = ModelBuildingPipeline()
        model_building_pipeline.main()
        logging.info(f"Completed {STAGE_NAME} Pipeline")

    except CustomException as e:
        raise CustomException(e, sys)