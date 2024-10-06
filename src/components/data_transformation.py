import os
import sys
from src.logger import logging
from src.exception import CustomException
from src import *
from src.utils.common import save_object, save_transformed_data
from src.entity.config_entity import DataTransformationConfig
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np

class DataTransformation:
    '''
    Class to transform the data and save the transformed data
    '''
    def __init__(self, 
                 config: DataTransformationConfig):
        
        self.config = config
    
    def create_preprocessor(self):
        '''
        This function creates a preprocessor object and saves it to the path specified in the configuration file

        Returns:
            - preprocessor: ColumnTransformer object

        Raises:
            - CustomException: If any error occurs while creating the preprocessor object
        '''
        try:
            logging.info("Specifying the numerical and categorical features")
            numerical_features = ['gpa', 'gmat', 'work_exp']
            categorical_features = [
                    'gender',
                    'international',
                    'major',
                    'race',
                    'work_industry'
            ]

            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='mean')),
                    ('scaler', StandardScaler())
                ]
            )

            logging.info("Successfully created numerical pipeline")


            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('encoder', OneHotEncoder(handle_unknown='ignore', drop='first', sparse_output=False))
                ]
            )

            logging.info("Successfully created categorical pipeline")


            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', num_pipeline, numerical_features),
                    ('cat', cat_pipeline, categorical_features)
                ]
            )

            logging.info("Successfully created column transformer")
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_data_transformation(self, training_data, testing_data):
        '''
        This function transforms the data using the preprocessor object

        Args:
            - training_data: path to the training data
            - testing_data: path to the testing data

        Returns:
            - train_arr: Transformed training data
            - test_arr: Transformed testing data
            - preprocessor_obj_path: Path to the preprocessor object

        Raises:
            - CustomException: If any error occurs while transforming the data or saving the preprocessor object
        '''
        try:
            train_data = pd.read_csv(training_data)
            test_data = pd.read_csv(testing_data)

            logging.info("Data has been read successfully for data transformation")

            train_data['admission'] = train_data['admission'].replace('', 'Reject').fillna('Reject')
            test_data['admission'] = test_data['admission'].replace('', 'Reject').fillna('Reject')

            logging.info("Successfully replaced missing values in the target feature")

            logging.info("Splitting the data into input features and target feature")

            train_input_features = train_data.drop(columns=['admission', 'application_id'], axis=1)
            train_target_feature = train_data['admission']

            test_input_features = test_data.drop(columns=['admission', 'application_id'], axis=1)
            test_target_feature = test_data['admission']

            preprocessor = self.create_preprocessor()
            
            logging.info("Preprocessor object has been initialized successfully")


            transformed_train_data = preprocessor.fit_transform(train_input_features)
            logging.info("Training data has been transformed successfully")


            transformed_test_data = preprocessor.transform(test_input_features)
            logging.info("Testing data has been transformed successfully")

            train_target_feature = train_target_feature.map({'Admit': 1, 'Reject': 0, 'Waitlist': 2})
            test_target_feature = test_target_feature.map({'Admit': 1, 'Reject': 0, 'Waitlist': 2})

            logging.info("Successfully mapped the target feature to numerical values for training and testing data")

            logging.info(f'Shape of transformed train data: {transformed_train_data.shape}')
            logging.info(f'Shape of transformed test data: {transformed_test_data.shape}')


            train_arr = np.c_[
                transformed_train_data,
                np.array(train_target_feature)
            ]

            test_arr = np.c_[
                transformed_test_data,
                np.array(test_target_feature)
            ]

            logging.info("Successfully concatenated the transformed data with the target feature for training and testing data")
 
            save_object(
                object= preprocessor, 
                object_path = self.config.preprocessor_obj_path
                )
            logging.info(f"Preprocessor object has been saved successfully at {self.config.preprocessor_obj_path}")

            save_transformed_data(
                data = train_arr, 
                path = self.config.train_arr
            )

            logging.info(f"Successfully saved transformed train data at {self.config.train_arr}")
            
            logging.info("Saving the transformed test data")
            save_transformed_data(
                data = test_arr,
                path = self.config.test_arr
            )

            logging.info(f"Successfully saved transformed test data at {self.config.test_arr}")


            logging.info("Returning the transformed data")

            return (
                train_arr,
                test_arr,
                self.config.preprocessor_obj_path
            )

        except Exception as e:
            raise CustomException(e, sys)