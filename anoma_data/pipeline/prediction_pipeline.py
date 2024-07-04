import os
import sys
import io
import numpy as np
import pandas as pd
from anoma_data.entity.config_entity import AnomaDataPredictorConfig
from anoma_data.entity.s3_estimator import AnomaDataEstimator
from anoma_data.exception import AnomaDataException
from anoma_data.logger import logging
from anoma_data.utils.main_utils import read_yaml_file,drop_columns
from pandas import DataFrame
from anoma_data.constants import PREDICTION_SCHEMA_FILE_PATH
from anoma_data.components.prediction_data_validation import PredictionDataValidation


class AnomaData:
    def __init__(self
             
        ):
        """
        Anoma Data constructor
        Input: all features of the trained model for prediction
        """
        try:
            
            self._schema_config =read_yaml_file(file_path=PREDICTION_SCHEMA_FILE_PATH)
           


        except Exception as e:
            raise AnomaDataException(e, sys) from e
        
    def data_transform(self,anomadata_input_df)-> DataFrame:
        drop_cols = self._schema_config['drop_columns']
        anomadata_input_df=drop_columns(anomadata_input_df,drop_cols)
        return anomadata_input_df

    def get_anomadata_input_data_frame(self,contents)-> DataFrame:
        """
        This function returns a DataFrame from AnomaData class input
        """
        try:
            
            #anomadata_input_dict = self.get_anoma_data_as_dict()
            anomadata_input_df=pd.read_csv(contents)
            #anomadata_input_df = pd.read_csv(io.BytesIO(contents))
            validation_error_msg = ""
            status=PredictionDataValidation().validate_number_of_columns(anomadata_input_df)
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."
            status=PredictionDataValidation().is_column_exist(anomadata_input_df)
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe."

            validation_status=len(validation_error_msg)==0
            logging.info(f'Validation status: {validation_status}')
            if validation_status:
                anomadata_input_df=self.data_transform(anomadata_input_df)
                return anomadata_input_df
            else:
                logging.info(f"Validation_error: {validation_error_msg}")
                raise AnomaDataException(f"Validation_error: {validation_error_msg}", sys)
        
        except Exception as e:
            raise AnomaDataException(e, sys) from e


    def get_anoma_data_as_dict(self):
        
        logging.info("Entered get_anoma_data_as_dict method as AnomaData class")

        try:
            input_data = {
              
            }

            logging.info("Created anoma data dict")

            logging.info("Exited get_anoma_data_as_dict method as AnomaData class")

            return input_data

        except Exception as e:
            raise AnomaDataException(e, sys) from e

class AnomaDataClassifier:
    def __init__(self,prediction_pipeline_config: AnomaDataPredictorConfig = AnomaDataPredictorConfig()) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction the value
        """
        try:
            # self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise AnomaDataException(e, sys)
        
    def convert_to_csv(self,path):
        
        df=pd.read_csv(path)
        return df

    def predict(self, dataframe) -> str:
        """
        This is the method of AnomaDataClassifier
        Returns: Prediction in string format
        """
        try:
            logging.info("Entered predict method of AnomaDataClassifier class")
            model = AnomaDataEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path
            )
            result =  model.predict(dataframe)
            
            return result
        
        except Exception as e:
            raise AnomaDataException(e, sys)
        

    def run_pipeline(self):
        """
        This method of AnomaDataClassifier class is responsible for running complete pipeline
        """
        try:
            logging.info("Entered run_pipeline method of AnomaDataClassifier class")
            df=self.convert_to_csv(self.prediction_pipeline_config.prediction_file_path)

            result=self.predict(df)
            logging.info("Exited run_pipeline method of AnomaDataClassifier class")
            return result
        except Exception as e:
            raise AnomaDataException(e, sys)
