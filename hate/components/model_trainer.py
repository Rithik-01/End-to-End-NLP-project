import os 
import sys
import pandas as pd
from hate.logger import logging
from hate.constants import *
from hate.exceptional import CustomException
from sklearn.model_selection import train_test_split
import tensorflow as tf
from hate.entity.config_entity import ModelTrainerConfig
from hate.entity.artifact_entity import ModelTrainerArtifacts,DataTransformationArtifacts
from hate.ml.model import ModelArchitecture

class ModelTrainer:
    def __init__(self,data_transformation_artifacts: DataTransformationArtifacts,
                model_trainer_config: ModelTrainerConfig):

        self.data_transformation_artifacts = data_transformation_artifacts
        self.model_trainer_config = model_trainer_config

    
    def spliting_data(self, csv_path):
        try:
            logging.info("Entered the spliting_data function")
            logging.info("Reading the data")
            df = pd.read_csv(csv_path, index_col=False)

            
            df.dropna(subset=[TWEET], inplace=True)
            df.reset_index(drop=True, inplace=True)

            logging.info("Splitting the data into x and y")
            x = df[TWEET].astype(str).values   
            y = df[LABEL].values               

            logging.info("Applying train_test_split on the data")
            x_train, x_test, y_train, y_test = train_test_split(
                x, y, test_size=0.3, random_state=42
            )

            print(len(x_train), len(y_train))
            print(len(x_test), len(y_test))
            print(type(x_train), type(y_train))

            logging.info("Exited the spliting_data function")
            return x_train, x_test, y_train, y_test

        except Exception as e:
            raise CustomException(e, sys) from e
        

    def vectorizer(self, x_train):
        try:
            logging.info("Applying tokenization on the data")
            text_vectorizer = tf.keras.layers.TextVectorization(
                max_tokens=self.model_trainer_config.MAX_WORDS,
                output_sequence_length=self.model_trainer_config.MAX_LEN,
                standardize='lower_and_strip_punctuation',
                split='whitespace',
                output_mode='int'
            )
            text_vectorizer.adapt(x_train)
            sequences_matrix = text_vectorizer(x_train).numpy()
            logging.info(f"converting text to sequences: {sequences_matrix[:2]}")
            logging.info(f"The sequence matrix is: {sequences_matrix}")
            return sequences_matrix, text_vectorizer
        
        except Exception as e:
            raise CustomException(e, sys) from e
    
        
    def initiate_model_trainer(self,) -> ModelTrainerArtifacts:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        """
        Method Name :   initiate_model_trainer
        Description :   This function initiates a model trainer steps
        
        Output      :   Returns model trainer artifact
        On Failure  :   Write an exception log and then raise an exception
        """

        try:
            logging.info("Entered the initiate_model_trainer function ")
            x_train,x_test,y_train,y_test = self.spliting_data(csv_path=self.data_transformation_artifacts.transformed_data_path)

            logging.info(f"Xtrain size is : {x_train.shape}")

            logging.info(f"Xtest size is : {x_test.shape}")

            sequences_matrix,text_vectorizer =self.vectorizer(x_train)

            model_architecture = ModelArchitecture(text_vectorizer)   

            model = model_architecture.get_model()

            logging.info("Entered into model training")
            model.fit(x_train, y_train, 
                        batch_size=self.model_trainer_config.BATCH_SIZE, 
                        epochs = self.model_trainer_config.EPOCH, 
                        validation_split=self.model_trainer_config.VALIDATION_SPLIT, 
                        )
            logging.info("Model training finished")
            os.makedirs(self.model_trainer_config.TRAINED_MODEL_DIR,exist_ok=True)


            logging.info("saving the model")
            model.save(self.model_trainer_config.TRAINED_MODEL_PATH, save_format="tf")

            pd.DataFrame(x_test, columns=["tweet"]).to_csv(self.model_trainer_config.X_TEST_DATA_PATH, index=False)
            pd.DataFrame(x_train, columns=["tweet"]).to_csv(self.model_trainer_config.X_TRAIN_DATA_PATH, index=False)
            
            pd.DataFrame(y_test, columns=["label"]).to_csv(self.model_trainer_config.Y_TEST_DATA_PATH, index=False)

            

            model_trainer_artifacts = ModelTrainerArtifacts(
                trained_model_path = self.model_trainer_config.TRAINED_MODEL_PATH,
                x_test_path = self.model_trainer_config.X_TEST_DATA_PATH,
                y_test_path = self.model_trainer_config.Y_TEST_DATA_PATH)
            logging.info("Returning the ModelTrainerArtifacts")
            return model_trainer_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e