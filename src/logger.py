import logging
import os
from datetime import datetime

# set log directory
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)

# set log file format
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# set log file name
log_file = os.path.join(log_dir, f'{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.log')

# log configuration
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format=log_format
)