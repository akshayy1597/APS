"""
from sensor.logger import logging
from sensor.exception import SensorException
import sys,os
from sensor.utils import dump_csv_file_to_mongodb_collection
from sensor.entity import config_entity 
from sensor.components.data_ingestion import DataIngestion
from sensor.pipeline.training_pipeline import TrainPipeline 

from sensor.configuration.mongo_db_connection import MongoDBClient



from sensor.utils import get_collection_as_dataframe
from sensor.entity.config_entity  import TrainingPipelineConfig,DataIngestionConfig
from sensor.components.data_validation import DataValidation
from sensor.components.data_transformation import DataTransformation
from sensor.components.model_trainer import ModelTrainer
from sensor.components.model_evaluation import ModelEvaluation

print(__name__)
if __name__=="__main__":  #exception shouldn't run directly but the given values should; also known as model execution control (prevent execution of code when imported)   #exception shouldn't run directly but the given values should; also known as model execution control (prevent execution of code when imported)
     file_path="/Users/akshayy/Desktop/APS/aps_failure_training_set1.csv" 
     database_name="ineuron"
     collection_name ="sensor"
     dump_csv_file_to_mongodb_collection(file_path,database_name,collection_name)
     
     try:
          training_pipeline_config = config_entity.TrainingPipelineConfig()

          #data ingestion
          data_ingestion_config  = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
          print(data_ingestion_config.to_dict())
          data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
          data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
          
          #data validation
          data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
          data_validation = DataValidation(data_validation_config=data_validation_config,
                         data_ingestion_artifact=data_ingestion_artifact)

          data_validation_artifact = data_validation.initiate_data_validation()

          #data transformation
          data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
          data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
          data_ingestion_artifact=data_ingestion_artifact)
          data_transformation_artifact = data_transformation.initiate_data_transformation()
          
          #model trainer
          model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
          model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
          model_trainer_artifact = model_trainer.initiate_model_trainer()

          model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
          model_eval  = ModelEvaluation(model_eval_config=model_eval_config,
           data_ingestion_artifact=data_ingestion_artifact,
           data_transformation_artifact=data_transformation_artifact,
            model_trainer_artifact=model_trainer_artifact)
          model_eval_artifact = model_eval.initiate_model_evaluation()

     except Exception as e:
         print(e)




if __name__ == "__main__":
    file_path="/Users/akshayy/Desktop/APS/aps_failure_training_set1.csv"
    database_name="ineuron"
    collection_name ="sensor"
    dump_csv_file_to_mongodb_collection(file_path,database_name,collection_name)

    training_pipeline = TrainPipeline()
    training_pipeline.run_pipeline()
"""




from sensor.configuration.mongodb_connection import MongoDBClient 
from sensor.exception import SensorException
import os , sys
from sensor.logger import logging
from sensor.pipeline.training_pipeline import TrainPipeline
#from  sensor.utils import dump_csv_file_to_mongodb_collecton
#from sensor.entity.config_entity  import TrainingPipelineConfig,DataIngestionConfig



# def test_exception():
#     try:
#         logging.info("ki yaha p bhaiaa ek error ayegi diveision by zero wali error ")
#         a=1/0
#     except Exception as e:
#        raise SensorException(e,sys) 



if __name__ == "__main__":

    # file_path="/Users/myhome/Downloads/sensorlive/aps_failure_training_set1.csv"
    # database_name="ineuron"
    # collection_name ="sensor"
    # dump_csv_file_to_mongodb_collection(file_path,database_name,collection_name)

    training_pipeline = TrainPipeline()
    training_pipeline.run_pipeline()



    # try:
    #     test_exception()
    # except Exception as e:
    #     print(e)










    