import logging  #this file is used to capture and maintain all the errors after the project is being deployed 
import os
from datetime import datetime
import os

#log file name
LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"

#log directory
LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")

#create folder if not available
os.makedirs(LOG_FILE_DIR,exist_ok=True)     #exist_ok=True means if the folder is already present then don't create it again
#os.makedirs(LOG_FILE_DIR)  #this will create the folder if not present 

#log file path

LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,  #log level (INFO, DEBUG, WARNING, ERROR, CRITICAL) debug being the smallest and critical being the largest
)