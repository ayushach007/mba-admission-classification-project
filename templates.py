import os
from pathlib import Path
import logging

# specify project name
project_name = 'mba_classification'

files = [
    f'src/{project_name}/__init__.py',
    f'src/{project_name}/logger.py',
    f'src/{project_name}/exception.py',
    f'src/{project_name}/utils.py',
    f'src/{project_name}/components/__init__.py',
    f'src/{project_name}/components/data_ingestion.py',
    f'src/{project_name}/components/data_transformation.py',
    f'src/{project_name}/components/model_training.py',
    f'src/{project_name}/components/model_evaluation.py',
    f'src/{project_name}/pipeline/training_pipeline.py',
    f'src/{project_name}/pipeline/predict_pipeline.py',
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
