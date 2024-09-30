from src.logger import logging
import sys
from src.exception import CustomException
from src.pipeline.stage_01_data_ingestion_pipeline import DataIngestionPipeline
from src.pipeline.stage_02_data_transformation_pipeline import DataTransformationPipeline
from src.pipeline.stage_03_model_building_and_evaluation import ModelBuildingPipeline



STAGE_NAME = "Data Ingestion"

try:
    logging.info(f"Starting : {STAGE_NAME}")
    data_ingestion_pipeline = DataIngestionPipeline()
    training_data, testing_data = data_ingestion_pipeline.main()
    logging.info(f"Completed {STAGE_NAME} Pipeline")

except CustomException as e:
    raise CustomException(e, sys)


STAGE_NAME = "Data Transformation"
try:
    logging.info(f"Starting {STAGE_NAME} Pipeline")
    data_transformation_pipeline = DataTransformationPipeline(training_data=training_data, testing_data=testing_data)
    train_arr, test_arr = data_transformation_pipeline.main()
    logging.info(f"Completed {STAGE_NAME} Pipeline")

except CustomException as e:
    raise CustomException(e, sys)



STAGE_NAME = "Model Building"

if __name__ == "__main__":
    try:
        logging.info(f"Starting {STAGE_NAME} Pipeline")
        model_building_pipeline = ModelBuildingPipeline(train_array=train_arr, test_arr=test_arr)
        model_building_pipeline.main()
        logging.info(f"Completed {STAGE_NAME} Pipeline")

    except CustomException as e:
        raise CustomException(e, sys)