from src.logger import logging
import sys
from src.exception import CustomException
from src.pipeline.stage_01_data_ingestion_pipeline import DataIngestionPipeline


STAGE_NAME = "Data Ingestion"

try:
    logging.info(f"Starting : {STAGE_NAME}")
    data_ingestion_pipeline = DataIngestionPipeline()
    data_ingestion_pipeline.main()
    logging.info(f"Completed {STAGE_NAME} Pipeline")

except CustomException as e:
    raise CustomException(e, sys)