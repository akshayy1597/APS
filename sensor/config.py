from dataclasses import dataclass
import os
import pymongo

@dataclass


class EnvironmentVariable:
    mongo_db_url:str = os.getenv("MONGO_DB_URL")    #os.getenv is used to read the environment



env_var = EnvironmentVariable()

mongo_client = pymongo.MongoClient(env_var.mongo_db_url)    #our connection "mongo_db_url" being inside a class, has to use an object 
#"env_var" to access it. 


#with the use of config.py and util.py we will be sending the data to the database