import pandas as pd
from src.utils.common import load_object
import sys
from src.logger import logging
from src.exception import CustomException
import warnings 

warnings.filterwarnings('ignore')


class CustomData:
    '''
    This class is used to create a custom data object which can be used to predict the target
    '''

    def __init__(self,
                 gender: str,
                 international: str,
                 gpa: float,
                 major: str,
                 race: str,
                 gmat: float,
                 work_exp: float,
                 work_industry: str):
        try:
            logging.info('Initializing CustomData object')
        
            self.gender = gender

            self.international = international

            self.gpa = gpa

            self.major = major

            self.race = race

            self.gmat = gmat

            self.work_exp = work_exp

            self.work_industry = work_industry

            logging.info('Successfully initialized CustomData object')

        except Exception as e:
            raise CustomException(str(e))


    def get_data_as_dataframe(self) -> pd.DataFrame:
        '''
        This function converts the input data to a pandas dataframe

        Returns:
            - pd.DataFrame : dataframe containing the input data

        Raises:
            - CustomException : if any error occurs while converting the input data to dataframe
        '''
        try:
            logging.info('Converting input data to dataframe')
            data = {
                "gender" : [self.gender],
                "international" : [self.international],
                "gpa" : [self.gpa],
                "major" : [self.major],
                "race" : [self.race],
                "gmat" : [self.gmat],
                "work_exp" : [self.work_exp],
                "work_industry" : [self.work_industry]
            }

            df = pd.DataFrame(data)

            logging.info('Successfully converted input data to dataframe')

            return df
        except Exception as e:
            raise CustomException(str(e))


class PredictionPipeline:
    '''
    This class is used to predict the target using the input features
    '''
    def __init__(self) -> None:
        pass

    def predict(self, features):
        '''
        This function predicts the target using the input features

        Args:
            - features : input features

        Returns:
            - prediction : predicted target

        Raises:
            - CustomException : if any error occurs while predicting the target
        '''
        try:
            logging.info('Prediction pipeline started')

            logging.info('loading preprocessor and model for prediction')
            preprocessor_path = 'artifacts/data_transformation/preprocessor.joblib'
            preprocessor = load_object(preprocessor_path)
            model = load_object('artifacts/model_training/model.pkl')

            logging.info('Successfully loaded preprocessor and model for prediction')

            logging.info('Transforming input features')
            scaled_features = preprocessor.transform(features)
            logging.info('Successfully transformed input features')

            logging.info('Predicting the target')
            prediction = model.predict(scaled_features)
            logging.info('Successfully predicted the target')

            return prediction
        except Exception as e:
            raise CustomException(e, sys)
    