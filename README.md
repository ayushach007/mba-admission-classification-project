# MBA Admission Predictor

This project predicts the admission chances of students applying for MBA programs. The model forecasts if the student will get **admission**, be **rejected**, or be placed on a **waitlist**. It is a multi-class classification project. The dataset was sourced from Kaggle and stored in MySQL for further use. The project also incorporates a CI/CD pipeline with GitHub Actions and a Docker setup for future AWS deployment.

## Table of Contents
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Installation Instructions](#installation-instructions)
- [Usage Instructions](#usage-instructions)
- [License](#license)
- [Future Improvements](#future-improvements)

## Project Overview
The MBA Admission Predictor is designed to predict whether a student will be accepted, waitlisted, or rejected for an MBA program. It uses several machine learning algorithms, and a model is selected based on the best accuracy after training. The project is built as a Streamlit app for easy user interaction, and though a Docker setup is prepared for deployment, the project is not yet deployed on AWS.

## Technologies Used
- **Python Libraries**: Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, Streamlit
- **Machine Learning Algorithms**: Linear Regression, Decision Tree, Random Forest, AdaBoost, Gradient Boosting, XGBoost, SVM, KNN
- **SQL**: MySQL
- **CI/CD**: GitHub Actions
- **Deployment**: 
    - Free: Streamlit
    - Paid: AWS

## Installation Instructions

### How to run?

1. **Clone the repository**

    ```bash
    https://github.com/ayushach007/mba-admission-classification-project
    ```

2. **Create Virtual Environment**:
   - Using Conda:
     ```bash
     conda create --name mba_predictor python=3.8
     ```
   - Using Python venv:
     ```bash
     python3 -m venv mba_predictor
     ```
3. **Activate Virtual Environment**:
   - Conda:
     ```bash
     conda activate mba_predictor
     ```
   - Python venv:
     ```bash
     source mba_predictor/bin/activate   # On Windows: mba_predictor\Scripts\activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Project**:
  - Git Bash:
   ```bash
    export MLFLOW_TRACKING_URI= YOUR PROJECT URI OF DagsHub 
  ```

  ```bash
    export MLFLOW_TRACKING_USERNAME= YOUR USERNAME OF DagsHub
  ```

  ```bash
    export MLFLOW_TRACKING_PASSWORD= YOUR PASSWORD OF DagsHub
  ```

  ```bash
    python main.py
  ```
    

6. **For Streamlit APP**:
     ```bash
     streamlit run app.py
     ```

---

## AWS-CICD-Deployment-with-Github-Actions

### 1. Login to AWS console.

### 2. Create IAM user for deployment

	#with specific access

	1. EC2 access : It is virtual machine

	2. ECR: Elastic Container registry to save your docker image in aws


	#Description: About the deployment

	1. Build docker image of the source code

	2. Push your docker image to ECR

	3. Launch Your EC2 

	4. Pull Your image from ECR in EC2

	5. Lauch your docker image in EC2

	#Policy:

	1. AmazonEC2ContainerRegistryFullAccess

	2. AmazonEC2FullAccess

	
### 3. Create ECR repo to store/save docker image
    - Save the URI: 

	
### 4. Create EC2 machine (Ubuntu) 

### 5. Open EC2 and Install docker in EC2 Machine:
	
	
	#optinal

	sudo apt-get update -y

	sudo apt-get upgrade
	
	#required

	curl -fsSL https://get.docker.com -o get-docker.sh

	sudo sh get-docker.sh

	sudo usermod -aG docker ubuntu

	newgrp docker
	
### 6. Configure EC2 as self-hosted runner:
    setting>actions>runner>new self hosted runner> choose os> then run command one by one


### 7. Setup github secrets:

    AWS_ACCESS_KEY_ID=

    AWS_SECRET_ACCESS_KEY=

    AWS_REGION = us-east-1

    AWS_ECR_LOGIN_URI = demo>>  566373416292.dkr.ecr.ap-south-1.amazonaws.com

    ECR_REPOSITORY_NAME = simple-app


## Usage Instructions
Once the project is up and running, users can input the following fields:
- **Gender**: Male/Female
- **International**: Boolean (True/False)
- **GPA**: Numeric
- **Major**: Subject/Field of Study
- **Race/Ethnicity**: Selection of Race
- **GMAT**: Numeric GMAT score
- **Work Experience**: Numeric number of years
- **Work Industry**: Industry of previous work experience

Upon clicking the "Predict" button, the app predicts whether the student will be admitted, rejected, or placed on the waitlist.

## License
This project is licensed under the **GNU General Public License**. See the [LICENSE](LICENSE) file for more information.

## Future Improvements
- Improve model accuracy through further hyperparameter tuning.
- Experiment with deep learning algorithms to enhance prediction performance.
