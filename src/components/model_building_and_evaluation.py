import sys
from src.logger import logging  
from src.exception import CustomException
from src import *
from src.utils.common import (save_object, 
                              eval_model, 
                              save_model_metrics)
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, 
                              GradientBoostingClassifier, 
                              AdaBoostClassifier)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from src.entity.config_entity import ModelTrainingConfig

class ModelBuilding:
    def __init__(self, config: ModelTrainingConfig):
        self.config = config

    def initiate_model_building(self, train_arr, test_arr):
        try:
            logging.info("Initiating model building process")
            logging.info("Splitting data into train and test sets")
            X_train = train_arr[:, :-1]
            y_train = train_arr[:, -1]
            X_test = test_arr[:, :-1]
            y_test = test_arr[:, -1]

            logging.info("Splitting has been done successfully")

            logging.info("Specifying models to be trained")

            models = {
                "LogisticRegression": LogisticRegression(),
                "RandomForestClassifier": RandomForestClassifier(),
                "DecisionTreeClassifier": DecisionTreeClassifier(),
                "GradientBoostingClassifier": GradientBoostingClassifier(),
                "AdaBoostClassifier": AdaBoostClassifier(),
                "SVC": SVC(),
                "KNeighborsClassifier": KNeighborsClassifier(),
                "XGBClassifier": XGBClassifier()
            }

            logging.info("Models have been specified successfully")

            logging.info("Hyperparameter tuning for models")

            params = {
                "LogisticRegression": {
                    "C": [0.01, 0.1, 1]
                },

                "RandomForestClassifier": {
                    "n_estimators": [100, 200, 300],
                    "max_depth": [5, 10, 15, 20]
                },  

                "DecisionTreeClassifier": {
                    "max_depth": [5, 10, 20, 30],
                    "min_samples_split": [ 5, 10, 15]
                },

                "GradientBoostingClassifier": {
                    "n_estimators": [100, 200, 300],
                    "learning_rate": [0.01, 0.1, 1]
                },

                "AdaBoostClassifier": {
                    "n_estimators": [50, 100, 200, 300],
                    "learning_rate": [0.01, 0.1, 1]
                },

                "SVC": {
                    "C": [0.01, 0.1, 1],
                    "degree": [3, 4, 5]
                },

                "KNeighborsClassifier": {
                    "n_neighbors": [3, 5, 7],
                    "weights": ['uniform', 'distance']
                },

                "XGBClassifier": {
                    "n_estimators": [100, 200, 300],
                    "learning_rate": [0.01, 0.1, 1]
                }
            }

            logging.info("Hyperparameter tuning has been done successfully")

            logging.info("Model training and evaluation")

            model_report: dict = eval_model(X_train, X_test, y_train, y_test, models, params)

            logging.info("Model training and evaluation has been done successfully")

            logging.info("Saving model and metrics")

            save_model_metrics(model_report, self.config.model_metrics_path)
            
            logging.info("Model and metrics have been saved successfully")

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = models[best_model_name]

            if best_model_score < 0.75:
                logging.warning("Model performance is below 75%. Please consider retraining the model")

            logging.info(f'The best model is {best_model_name} with an accuracy score of {best_model_score}')

            logging.info("Saving the best model")
            save_object(
                object = best_model,
                object_path = self.config.model_path
            )

            logging.info("Model has been saved successfully")

            return best_model, best_model_score

        except Exception as e:
            raise CustomException(e, sys)
        