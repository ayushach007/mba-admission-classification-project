import os
from pathlib import Path
import logging

# specify project name
project_name = 'mba_classification'

files = [
    'src/__init__.py',
    'src/logger.py',
    'src/exception.py',
    'src/components/__init__.py',
    'src/components/data_ingestion.py',
    'src/components/data_transformation.py',
    'src/components/model_building_and_evaluation.py',
    'src/pipeline/__init__.py'
    'src/pipeline/stage_01_data_ingestion_pipeline.py',
    'src/pipeline/stage_02_data_transformation_pipeline.py',
    'src/pipeline/stage_03_model_building_and_evaluation.py',
    'src/pipeline/stage_04_predict_pipeline.py',
    'src/config/__init__.py',
    'src/config/configuration.py',
    'src/entity/__init__.py',
    'src/entity/config_entity.py',
    'src/utils/__init__.py',
    'src/utils/common.py',
    'notebooks/EDA.ipynb',
    'notebooks/model_building.ipynb',
    'notebooks/01_data_ingestion.ipynb',
    'notebooks/02_data_transformation.ipynb',
    'notebooks/03_model_training_and_evaluation.ipynb'
    'notebooks/04_predict_pipeline.ipynb',
    '.github/workflows/main.yaml',
    'config/config.yaml',
    '.env'
    'Dockerfile',
    'requirements.txt',
    'README.md',
    '.gitignore',
    'setup.py',
    'app.py',
    'main.py'
    'templates.py'
]

def create_files():
    '''
    This function creates all the files and directories specified in the files list
    '''
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
