import os
import sys
import yaml
from box.exceptions import BoxValueError
from box import ConfigBox
from pathlib import Path
from src.logger import logging
from src.exception import CustomException
from ensure import ensure_annotations
import joblib
import mysql.connector as mysql
from dotenv import load_dotenv
import pandas as pd

load_dotenv()


@ensure_annotations
def read_yaml_file(yamal_file_path: Path) -> ConfigBox:
    '''Reads a yaml file and returns the content as a dictionary

    Args:
        file_path (str): Path to the yaml file

    Raises:
        ValueError: If the yaml file is empty
        CustomException: If there is an error reading the file

    Returns:
        ConfigBox: ConfigBox object containing the content of the yaml file
    '''
    try:
        with open(yamal_file_path, 'r') as file:
            content =  yaml.safe_load(file)
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise CustomException(e, sys)
    

@ensure_annotations
def create_directory(path_to_directories: list, verbose: bool = True):
    '''Create list of directories

    Args:
        path_to_directories (list): List of paths to the directories to be created
        verbose (bool, optional): If True, logs the directory creation. Defaults to True.

    Raises:
        CustomException: If there is an error creating the directory
    '''
    try:
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
            if verbose:
                logging.info(f"Directory created at path {path}")
    except Exception as e:
        raise CustomException(e, sys)
    

@ensure_annotations
def save_object(object, model_path: Path, verbose: bool = True):
    '''Save the object as a joblib file

    Args:
        model (object): Model to be saved
        model_path (str): Path to save the model
        verbose (bool, optional): If True, logs the model saving. Defaults to True.

    Raises:
        CustomException: If there is an error saving the model
    '''
    try:
        joblib.dump(object, model_path)
        if verbose:
            logging.info(f"Model saved at path {model_path}")
    except Exception as e:
        raise CustomException(e, sys)
    
@ensure_annotations
def read_sql_data():
    '''Read data from a SQL database

    Returns:
        pd.DataFrame: Data read from the database

    Raises:
        CustomException: If there is an error reading the data
    '''
    try:
        logging.info("Reading data from SQL database")
        conn = mysql.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')
        )

        data = pd.read_sql("SELECT * FROM admission", conn)
        logging.info("Successfully read data from SQL database")
        return data
    except Exception as ex:
        raise CustomException(ex)