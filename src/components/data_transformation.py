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
    def __init__(self, 
                 config: DataTransformationConfig):
        
        self.config = config
    
    def create_preprocessor(self):
        '''
        This function creates a preprocessor object and saves it to the path specified in the configuration file

        Returns:
        preprocessor: ColumnTransformer object
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

            logging.info("Creating a numerical pipeline")
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='mean')),
                    ('scaler', StandardScaler())
                ]
            )

            logging.info("Successfully created numerical pipeline")

            logging.info("Creating a categorical pipeline")
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('encoder', OneHotEncoder(handle_unknown='ignore', drop='first', sparse_output=False))
                ]
            )

            logging.info("Successfully created categorical pipeline")

            logging.info("Creating a column transformer")
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', num_pipeline, numerical_features),
                    ('cat', cat_pipeline, categorical_features)
                ]
            )

            logging.info("Successfully created column transformer")

            logging.info("Saving the preprocessor object to the specified path")
            save_object(
                object= preprocessor, 
                object_path = self.config.preprocessor_obj_path
                )
            logging.info("Preprocessor object has been saved successfully")

            logging.info("Returning the preprocessor object")
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_data_transformation(self, training_data, testing_data):
        '''
        This function transforms the data using the preprocessor object

        Returns:
        transformed_data: DataFrame
        '''
        try:
            logging.info("Reading the training and testing data")
            train_data = pd.read_csv(training_data)
            test_data = pd.read_csv(testing_data)

            logging.info("Data has been read successfully")

            logging.info("Replacing empty strings with 'Rejected' in the admission column")
            train_data['admission'] = train_data['admission'].replace('', 'Rejected')
            test_data['admission'] = test_data['admission'].replace('', 'Rejected')

            logging.info("Splitting the data into input features and target feature")
            target = ['admission']

            train_input_features = train_data.drop(columns=['admission', 'application_id'], axis=1)
            train_target_feature = train_data[target]

            test_input_features = test_data.drop(columns=['admission', 'application_id'], axis=1)
            test_target_feature = test_data[target]

            logging.info("Initializing the preprocessor object")
            preprocessor = self.create_preprocessor()
            
            logging.info("Preprocessor object has been initialized successfully")

            logging.info("Transforming the training data")
            transformed_train_data = preprocessor.fit_transform(train_input_features)
            logging.info("Training data has been transformed successfully")

            logging.info("Transforming the testing data")
            transformed_test_data = preprocessor.transform(test_input_features)
            logging.info("Testing data has been transformed successfully")

            logging.info("Initializing the target encoder")
            target_encoder = LabelEncoder()

            logging.info("Fitting the target encoder on the training target feature")
            target_encoder.fit(train_target_feature)

            logging.info("Transforming the training target feature")
            transformed_train_target = target_encoder.transform(train_target_feature)


            logging.info("Combining the transformed training data and target feature")
            train_arr = np.c_[
                transformed_train_data,
                transformed_train_target
            ]

            logging.info("Combining the transformed testing data and target feature")
            test_arr = np.c_[
                transformed_test_data,
                test_target_feature
            ]

            logging.info("Saving the transformed trained data")
            save_transformed_data(
                data = train_arr, 
                path = self.config.train_arr
            )

            logging.info("Succesfully saved transformed train data")
            
            logging.info("Saving the transformed test data")
            save_transformed_data(
                data = test_arr,
                path = self.config.test_arr
            )

            logging.info("Succesfully saved transformed train data")


            logging.info("Returning the transformed data")

            return train_arr, test_arr

        except Exception as e:
            raise CustomException(e, sys)