from setuptools import setup, find_packages

HYPHEN_DOT_E = '-e .'

def get_requirements(file_path: str) -> list:
    '''
    This function reads the requirements.txt file and returns the list of requirements

    Args:
        - file_path: str: path to requirements.txt file

    Returns:
        - list: list of requirements
    '''
    with open(file_path, 'r') as f:
        requirements = f.readlines()
        requirements = [req.replace('\n', '') for req in requirements]

        if HYPHEN_DOT_E in requirements:
            requirements.remove(HYPHEN_DOT_E)

    return requirements

setup(
    name='mba_classification',
    version='0.1',
    description='A package for classification of MBA students',
    author='ayushach007',
    author_email='ayushach007@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)