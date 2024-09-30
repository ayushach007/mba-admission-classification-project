import os
import sys
import yaml
from box.exceptions import BoxValueError
from box import ConfigBox
from pathlib import Path
from src.logger import logging
from src.exception import CustomException
from ensure import ensure_annotations
import pickle
import mysql.connector as mysql
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import json

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
def save_object(object, object_path: str, verbose: bool = True):
    '''Save the object as a joblib file

    Args:
        object: Object to be saved
        object_path (str): Path to save the object
        verbose (bool, optional): If True, logs the object saving. Defaults to True.

    Raises:
        CustomException: If there is an error saving the model
    '''
    try:
        logging.info(f"Saving model at path {object_path}")
        with open(object_path, 'wb') as file:
            pickle.dump(object, file)
        if verbose:
            logging.info(f"Model saved at path {object_path}")

    except Exception as e:
        raise CustomException(e, sys)

@ensure_annotations
def load_object(object_path: str):
    '''Load the model from the joblib file

    Args:
        object_path (str): Path to the joblib file

    Returns:
        object: Model loaded from the joblib file

    Raises:
        CustomException: If there is an error loading the model
    '''
    try:
        logging.info(f"Loading model from path {object_path}")
        with open(object_path, 'rb') as file:
            object = pickle.load(file)
        logging.info(f"Model loaded from path {object_path}")
        return object
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
    
@ensure_annotations
def save_transformed_data(data, path):
    '''
    This function saves the transformed data to the specified path

    Args:
        data: Data to be saved
        path: Path to save the data
        preprocessors: Preprocessor object used to transform the data
    '''
    try:
        logging.info(f"Saving transformed data to path {path}")
        data = pd.DataFrame(data)
        data.to_csv(path, index=False, header=True)
        logging.info(f"Data saved to path {path}")
    except Exception as e:
        raise CustomException(e, sys)
    
@ensure_annotations
def eval_model(X_train, X_test, y_train, y_test, models, param):
    '''
    This method evaluates the performance of the models on the test data.
    
    Args:
    X_train: np.ndarray
        The input features of the training data
    X_test: np.ndarray
        The input features of the test data
    y_train: np.ndarray
        The target feature of the training data
    y_test: np.ndarray
        The target feature of the test data
    models: dict
        The dictionary containing the model objects
    param: dict
        The dictionary containing the hyperparameters for the models

    Returns:
    report: dict
        The dictionary containing the model names and their corresponding accuracy scores
    '''
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            params = list(param.values())[i]

            print(i, model, params)

            gs = GridSearchCV(model, params, cv=5)
            gs.fit(X_train, y_train)

            # select the best parameters
            best_params = gs.best_params_
            model.set_params(**best_params)

            model = model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_accuracy = accuracy_score(y_train, y_train_pred)
            test_model_accuracy = accuracy_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_accuracy

        return report

    except Exception as e:
        raise CustomException(e, sys)
    
@ensure_annotations
def save_model_metrics(report, path):
    '''
    This function saves the model metrics to the specified path in json format

    Args:
        report: dict
            The dictionary containing the model names and their corresponding accuracy scores
        path: str
            Path to save the model metrics

    Raises:
        CustomException: If there is an error saving the model metrics
    '''
    try:
        logging.info(f"Saving model metrics to path {path}")
        with open(path, 'w') as f:
            json.dump(report, f)
        logging.info(f"Model metrics saved to path {path}")
    except Exception as e:
        raise CustomException(e, sys)
    
