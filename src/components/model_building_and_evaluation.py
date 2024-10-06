import sys
from src.logger import logging  
from src.exception import CustomException
from src import *
from src.utils.common import (save_object, 
                              eval_model, 
                              save_model_metrics)
from imblearn.over_sampling import SMOTE
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, 
                              GradientBoostingClassifier, 
                              AdaBoostClassifier)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from src.entity.config_entity import ModelTrainingConfig
from urllib.parse import urlparse
import mlflow
class ModelBuilding:
    '''
    This class is responsible for building models, hyperparameter tuning, training and evaluating models, saving models and metrics, and saving the best model
    '''
    def __init__(self, config: ModelTrainingConfig):
        self.config = config

    def initiate_model_building(self, train_arr, test_arr):
        '''
        This function initiates model building process, splits data into train and test sets, specifies models to be trained, hyperparameter tuning for models, model training and evaluation, saves model and metrics, and saves the best model
        
        Args:
            - train_arr: Training data
            - test_arr: Testing data
            
        Returns:
            - best_model: Best model
            - best_model_score: Best model score
            
        Raises:
            - CustomException: If any error occurs while initiating model building or saving the best model
        '''

        try:
            logging.info("Initiating model building process")
            logging.info("Splitting data into train and test sets")
            X_train = train_arr[:, :-1]
            y_train = train_arr[:, -1]
            X_test = test_arr[:, :-1]
            y_test = test_arr[:, -1]


            # doing oversampling as the data is imbalanced
            sm = SMOTE(random_state=42)
            logging.info("Oversampling the data")

            X_train, y_train = sm.fit_resample(X_train, y_train)

            logging.info("Oversampling has been done successfully")

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

            # Evaluate models
            training_metrics, test_metrics = eval_model(X_train, X_test, y_train, y_test, models, params)

            logging.info("Model training and evaluation has been done successfully")

            logging.info("Saving model and metrics")
            
            # Save model metrics
            save_model_metrics(
                report = training_metrics,
                path = self.config.training_metrics
            )

            save_model_metrics(
                report = test_metrics,
                path = self.config.test_metrics
            )

            
            logging.info("Model and metrics have been saved successfully")

            # Select the best model based on test accuracy
            best_model_score = max(test_metrics.values(), key=lambda x: x['accuracy'])['accuracy']
            best_model_name = max(test_metrics, key=lambda x: test_metrics[x]['accuracy'])

            best_model = models[best_model_name]

            actual_model = ""
            for model in models:
                if model == best_model_name:
                    actual_model = actual_model + model
                                                            
            mlflow.set_registry_uri("https://dagshub.com/ayushach007/mba-admission-classification-project.mlflow")
            tracking_uri_type = urlparse(mlflow.get_registry_uri()).scheme

            # mlflow tracking
            with mlflow.start_run():
                mlflow.log_param("Model Name", best_model_name)
                mlflow.log_param("Best Parameters", test_metrics[best_model_name]['best_params'])
                mlflow.log_metric("Accuracy", test_metrics[best_model_name]['accuracy'])
                mlflow.log_metric("Precision", test_metrics[best_model_name]['precision'])
                mlflow.log_metric("Recall", test_metrics[best_model_name]['recall'])
                mlflow.log_metric("F1 Score", test_metrics[best_model_name]['f1_score'])
                # mlflow.log_metric("Confusion Matrix", test_metrics[best_model_name]['confusion_matrix'])

            if tracking_uri_type != "file":
                mlflow.sklearn.log_model(best_model, "model", registered_model_name=actual_model)
            else:
                mlflow.sklearn.log_model(best_model, "model")


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
        