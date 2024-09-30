# create streamlit app for prediction

import os
import sys
from src.exception import CustomException
from src.logger import logging
from src.pipeline.stage_04_predict_pipeline import CustomData, PredictionPipeline
import pandas as pd
import streamlit as st

def app():
    '''
    This function is used to create a streamlit app for prediction, it takes input features from the user and predicts the output

    Returns:
       - Predicted output

    Raises:
        - CustomException: If any error occurs while creating the streamlit app or predicting the output
    '''
    try:
        # create title inthe center using markdown
        st.markdown("<h1 style='text-align: center;'>MBA Admission Predictor</h1>", unsafe_allow_html=True)

        with open('styles.css') as f:
            css = f.read()
        
        # Apply the styles
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

        logging.info('Taking input features from the user')

        _, main_col, _ = st.columns([0.5, 3, 0.5])

        with main_col:
            
            with st.container():
                gen_col, int_col = st.columns(2)
                gpa_col, major_col = st.columns(2)
                race_col, gmat_col = st.columns(2)
                work_exp_col, work_ind_col = st.columns(2)
                
                with gen_col:
                    gender = st.selectbox(
                        label= "**Gender**",
                        options= ["", "Male", 'Female']
                    )

                with int_col:
                    international = st.selectbox(
                        label= "**International**",
                        options= ["", "True", 'False']
                    )

                with gpa_col:
                    gpa = st.number_input(
                        label= "**GPA**",
                        value= None,
                        min_value= 0.0,
                        max_value= 4.0,
                        step= 0.1
                    )


                with major_col:
                    major = st.selectbox(
                        label= "**Major**",
                        options= ["", 'Business', 'Humanities', 'STEM'] 
                    )

                with race_col:
                    race = st.selectbox(
                        label= "**Race**",
                        options= ["", 'White', 'Asian', 'Hispanic', 'Black', 'Other']
                    )

                with gmat_col:
                    gmat = st.number_input(
                        label= "**GMAT**",
                        value= None,
                        min_value= 200,
                        max_value= 800,
                        step= 1
                    )

                with work_exp_col:
                    work_exp = st.number_input(
                        label= "**Work Experience**",
                        value= None,
                        min_value= 0,
                        max_value= 20,
                        step= 1
                    )

                with work_ind_col:
                    work_industry = st.selectbox(
                        label= "**Work Industry**",
                        options= ["", 'Financial Services', 'Investment Management', 'Technology', 'Consulting','Nonprofit/Gov', 'PE/VC', 'Health Care', 'Investment Banking', 'Other', 'Retail', 'Energy', 'CPG', 'Real Estate', 'Media/Entertainment']
                    )

                logging.info('Successfully took input features from the user')

                if 'predict_output' not in st.session_state:
                    st.session_state.predict_output = False
                
                if st.button('Predict',type='primary'):
                    st.session_state.predict_output = not st.session_state.predict_output

                if st.session_state.predict_output:
                    if all([
                        gender, international, gpa, major, race, gmat, work_exp, work_industry
                    ]):
                        data = CustomData(
                            gender= gender,
                            international= international,
                            gpa= gpa,
                            major= major,
                            race=race,
                            gmat=gmat,
                            work_exp=work_exp,
                            work_industry=work_industry
                        )

                        data = data.get_data_as_dataframe()

                        pred_pipeline = PredictionPipeline()

                        pred = pred_pipeline.predict(data)

                        # convert the prediction into readable format like 0 for admit and 1 for reject and 2 for waitlist
                        if pred == 0:
                            st.success(':smile: Congratulations! You are Admitted')
                        elif pred == 1:
                            st.info('Sorry! You are Rejected')
                        elif pred == 2:
                            st.info(':expressionless: You are in Waitlist')
                        else:
                            st.error(':warning: Prediction not found for the given input')
                    else:
                        st.info(":warning: Please fill all the fields")

    except Exception as e:
        raise CustomException(e, sys)
    
if __name__ == '__main__':
    logging.info('Starting the streamlit app')
    app()