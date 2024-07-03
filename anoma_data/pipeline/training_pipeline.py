import sys
from anoma_data.exception import AnomaDataException
from anoma_data.logger import logging
import numpy as np
from anoma_data.components.data_ingestion import DataIngestion

from anoma_data.components.data_validation import DataValidation
from anoma_data.components.data_transformation import DataTransformation
from anoma_data.components.model_trainer import ModelTrainer
from anoma_data.components.model_evaluation import ModelEvaluation
from anoma_data.components.model_pusher import ModelPusher

from anoma_data.entity.config_entity import (DataIngestionConfig,
                                             DataValidationConfig,
                                             DataTransformationConfig,
                                             ModelTrainerConfig,
                                             ModelEvaluationConfig,
                                             ModelPusherConfig)
                                     

from anoma_data.entity.artifact_entity import (DataIngestionArtifact,
                                               DataValidationArtifact,
                                               DataTransformationArtifact,
                                               ModelTrainerArtifact,
                                               ModelEvaluationArtifact,
                                               ModelPusherArtifact,
                                               ClassificationMetricArtifact)
                                          


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()
        
        self.model_pusher_config = ModelPusherConfig()


    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        """
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )
            return data_ingestion_artifact
        except Exception as e:
            raise AnomaDataException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data validation component
        """
        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config
                                             )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")

            logging.info(
                "Exited the start_data_validation method of TrainPipeline class"
            )

            return data_validation_artifact

        except Exception as e:
            raise AnomaDataException(e, sys) from e
        
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data transformation component
        """
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                     data_transformation_config=self.data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise AnomaDataException(e, sys)
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        """
        This method of TrainPipeline class is responsible for starting model training
        """
        try:
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=self.model_trainer_config
                                         )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise AnomaDataException(e, sys)
        
    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact,
                               model_trainer_artifact: ModelTrainerArtifact,
                               data_transformation_artifact: DataTransformationArtifact) -> ModelEvaluationArtifact:
        """
        This method of TrainPipeline class is responsible for starting modle evaluation
        """
        try:
            model_evaluation = ModelEvaluation(model_eval_config=self.model_evaluation_config,
                                               data_ingestion_artifact=data_ingestion_artifact,
                                               model_trainer_artifact=model_trainer_artifact,
                                               data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()
            return model_evaluation_artifact
        except Exception as e:
            raise AnomaDataException(e, sys)
        
    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifact) -> ModelPusherArtifact:
        """
        This method of TrainPipeline class is responsible for starting model pushing
        """
        try:
            model_pusher = ModelPusher(model_evaluation_artifact=model_evaluation_artifact,
                                       model_pusher_config=self.model_pusher_config
                                       )
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
        except Exception as e:
            raise AnomaDataException(e, sys)
            
        
    
    def run_pipeline(self, ) -> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

            """Testing the pipeline of model evaluation and pusher by bypassing previous steps

            data_ingestion_artifact = DataIngestionArtifact('/Users/skt/Documents/MLOPS Projects/AnomaData-Machine-Anomaly-Detection/artifact/07_03_2024_16_44_18/data_ingestion/ingested/train.csv',
                                                            '/Users/skt/Documents/MLOPS Projects/AnomaData-Machine-Anomaly-Detection/artifact/07_03_2024_16_44_18/data_ingestion/ingested/test.csv')
            
            model_trainer_artifact=ModelTrainerArtifact('/Users/skt/Documents/MLOPS Projects/AnomaData-Machine-Anomaly-Detection/artifact/07_03_2024_16_44_18/model_trainer/trained_model/model.pkl',
                                                        ClassificationMetricArtifact(0.8409777533644603,
                                                                                     np.float64(0.812863606981254),
                                                                                     np.float64(0.9940711462450593),
                                                                                     np.float64(0.6875341716785128)))
            data_transformation_artifact=DataTransformationArtifact('/Users/skt/Documents/MLOPS Projects/AnomaData-Machine-Anomaly-Detection/artifact/07_03_2024_16_44_18/data_transformation/transformed_object/preprocessing.pkl',
                                                                    '/Users/skt/Documents/MLOPS Projects/AnomaData-Machine-Anomaly-Detection/artifact/07_03_2024_16_44_18/data_transformation/transformed/train.npy',
                                                                    '/Users/skt/Documents/MLOPS Projects/AnomaData-Machine-Anomaly-Detection/artifact/07_03_2024_16_44_18/data_transformation/transformed/test.npy')"""
            
            model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                                    model_trainer_artifact=model_trainer_artifact,
                                                                    data_transformation_artifact=data_transformation_artifact)
            
            if not model_evaluation_artifact.is_model_accepted:
                logging.info(f"Model not accepted.")
                return None
            else:
                model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)


        
        except Exception as e:
            raise AnomaDataException(e, sys)
        

