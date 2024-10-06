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

        st.set_page_config(page_title='MBA Admission Predictor', page_icon=':mortar_board:', layout='centered', initial_sidebar_state='auto')

        # create title inthe center using markdown
        st.markdown("<h1 style='text-align: center;'>MBA Admission Predictor</h1>", unsafe_allow_html=True)


        _, main_col, _ = st.columns([0.5, 3, 0.5])

        with main_col:
            
            with st.container(border=True):
                gen_col, _, int_col = st.columns([2, 0.4, 2])
                gpa_col, _, major_col = st.columns([2, 0.4, 2])
                race_col, _, gmat_col = st.columns([2, 0.4, 2])
                work_exp_col, _, work_ind_col = st.columns([2, 0.4, 2])
                
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
                            st.info(':disappointed: Sorry! You are Rejected')
                        elif pred == 1:
                            st.info(':smiley: Congratulations! You are Admitted')
                        elif pred == 2:
                            st.info(':neutral_face: You are in the waitlist')
                        else:
                            st.error(':warning: Prediction not found for the given input')
                    else:
                        st.info(":warning: Please fill all the fields")
                
            # at the end of the app, display the author name
            st.markdown("<h5 style='text-align: left;'>Created by : <a href='https://www.linkedin.com/in/ayush-acharya-912955282/'>Ayush Acharya</a></h4>", unsafe_allow_html=True)

    except Exception as e:
        raise CustomException(e, sys)
    
if __name__ == '__main__':
    logging.info('Starting the streamlit app')
    app()