import os
from pathlib import Path
import logging

# specify project name
project_name = 'mba_classification'

files = [
    'src/__init__.py',
    'src/logger.py',
    'src/exception.py',
    'src/utils.py',
    'src/components/__init__.py',
    'src/components/data_ingestion.py',
    'src/components/data_transformation.py',
    'src/components/model_training.py',
    'src/components/model_evaluation.py',
    'src/pipeline/training_pipeline.py',
    'src/pipeline/predict_pipeline.py',
    'notebooks/EDA.ipynb',
    'notebooks/model_building.ipynb',
    'notebooks/01_data_ingestion.ipynb',
    'notebooks/02_data_transformation.ipynb',
    'notebooks/03_model_training.ipynb',
    'notebooks/04_model_evaluation.ipynb',
    'notebooks/05_predict_pipeline.ipynb',
    '.github/workflows/main.yaml',
    'Dockerfile',
    'requirements.txt',
    'README.md',
    '.gitignore',
    'setup.py',
    'app.py',
    'templates.py'
]

def create_files():
    for file in files:
        file = Path(file)
        file_dir, file_name = os.path.split(file)

        if file_dir != '':
            os.makedirs(file_dir, exist_ok=True)
            logging.info(f'{file_dir} created for {file_name}')

        if not os.path.exists(file) or os.path.getsize(file) == 0:
            with open(file, 'w') as f:
                # File is intentionally left empty
                f.write('')
        else:
            logging.info(f'{file} already exists')

        logging.info(f'{file} created')

if __name__ == '__main__':
    create_files()
    logging.info('All files created successfully')
