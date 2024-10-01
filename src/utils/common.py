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
# import percision, recall, f1_score, confusion_matrix
from sklearn.metrics import precision_score, recall_score,f1_score, confusion_matrix
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
def eval_model(X_train, X_test, y_train, y_test, models, params):
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
        training_metrics = {}
        test_metrics = {}

        for i in range(len(list(models))):
            model_name = list(models.keys())[i]
            model = models[model_name]
            param = params[model_name]

            print(i, model, param)

            gs = GridSearchCV(model, param, cv=5)
            gs.fit(X_train, y_train)

            # select the best parameters
            best_params = gs.best_params_
            model.set_params(**best_params)

            model = model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_accuracy = accuracy_score(y_train, y_train_pred)
            test_model_accuracy = accuracy_score(y_test, y_test_pred)

            train_model_precision = precision_score(y_train, y_train_pred, average='weighted')
            test_model_precision = precision_score(y_test, y_test_pred, average='weighted')

            train_model_recall = recall_score(y_train, y_train_pred, average='weighted')
            test_model_recall = recall_score(y_test, y_test_pred, average='weighted')

            train_model_f1_score = f1_score(y_train, y_train_pred, average='weighted')
            test_model_f1_score = f1_score(y_test, y_test_pred, average='weighted')

            train_model_confusion_matrix = confusion_matrix(y_train, y_train_pred).tolist()
            test_model_confusion_matrix = confusion_matrix(y_test, y_test_pred).tolist()

            

            training_metrics[model_name] = {
                "accuracy": train_model_accuracy,
                "precision": train_model_precision,
                "recall": train_model_recall,
                "f1_score": train_model_f1_score,
                "confusion_matrix": train_model_confusion_matrix,
                "best_params": best_params
            }

            test_metrics[model_name] = {
                "accuracy": test_model_accuracy,
                "precision": test_model_precision,
                "recall": test_model_recall,
                "f1_score": test_model_f1_score,
                "confusion_matrix": test_model_confusion_matrix,
                "best_params": best_params
            }

        return training_metrics, test_metrics

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
        # Convert any non-serializable objects to serializable format
        serializable_report = {}
        for model_name, metrics in report.items():
            serializable_metrics = {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in metrics.items()}
            serializable_metrics["model"] = model_name
            serializable_report[model_name] = serializable_metrics

        logging.info(f"Saving model metrics to path {path}")
        with open(path, 'w') as f:
            json.dump(serializable_report, f, indent=4, sort_keys=True)
        logging.info(f"Model metrics saved to path {path}")
    except Exception as e:
        raise CustomException(e, sys)
