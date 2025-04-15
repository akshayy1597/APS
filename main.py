"""
from sensor.logger import logging
from sensor.exception import SensorException
import sys,os
from sensor.utils import dump_csv_file_to_mongodb_collection
from sensor.entity import config_entity 
from sensor.components.data_ingestion import DataIngestion
from sensor.pipeline.training_pipeline import TrainPipeline 
#from  sensor.utils import dump_csv_file_to_mongodb_collecton
#from sensor.entity.config_entity  import TrainingPipelineConfig,DataIngestionConfig
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
from sensor.utils.main_utils import load_object
from sensor.ML.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import SAVED_MODEL_DIR



from  fastapi import FastAPI
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run  #uvicorn is our server 
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import FastAPI, File, UploadFile, Response 
import pandas as pd

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd
import sys
import io
sys.path.append(os.getcwd()) 
import chardet 



app = FastAPI()


origins = ["*"]
#Cross-Origin Resource Sharing (CORS) 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/",tags=["authentication"])
async def  index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train():
    try:

        training_pipeline = TrainPipeline()

        if training_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")    #for fastapi, we return through response  
        training_pipeline.run_pipeline()
        return Response("Training successfully completed!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")
    

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Optional: detect encoding (sometimes helps)
        detected = chardet.detect(contents)
        encoding = detected.get("encoding", "utf-8")


        # Try to parse the CSV safely
        try:
            df = pd.read_csv(
                io.StringIO(contents.decode(encoding)),
                sep=",",  # or try sep=None to auto-detect
                engine="python",  # more tolerant parser
                on_bad_lines='skip'  # pandas 1.3+
            )
        except Exception as parse_err:
            raise Exception(f"CSV Parsing Failed: {parse_err}")

        # Check if data was actually read
        if df.empty:
            return JSONResponse(content={"error": "CSV file is empty or badly formatted."}, status_code=400)

        # Load model
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return JSONResponse(content={"error": "Model is not available"}, status_code=404)

        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)

        # Perform prediction
        y_pred = model.predict(df)
        df["predicted_column"] = y_pred
        df["predicted_column"].replace(TargetValueMapping().reverse_mapping, inplace=True)

        return {
            "message": "CSV successfully processed.",
            "rows": len(df),
            "preview": df.head().to_dict(orient="records")
        }
         
        

    except Exception as e:
        raise SensorException(e, sys)  
    

def main():
    try:
            
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)



# def test_exception():
#     try:
#         logging.info("ki yaha p bhaiaa ek error ayegi diveision by zero wali error ")
#         a=1/0
#     except Exception as e:
#        raise SensorException(e,sys) 



if __name__ == "__main__":
    app_run(app ,host=APP_HOST,port=APP_PORT) 

    # file_path="/Users/myhome/Downloads/sensorlive/aps_failure_training_set1.csv"
    # database_name="ineuron"
    # collection_name ="sensor"
    # dump_csv_file_to_mongodb_collection(file_path,database_name,collection_name)

    #training_pipeline = TrainPipeline()
    #training_pipeline.run_pipeline()



    # try:
    #     test_exception()
    # except Exception as e:
    #     print(e)








    