import os
import sys
from hate.logger import logging
from hate.exceptional import CustomException
from hate.entity.config_entity import DataValidationCongif
import pandas as pd


class DataValidation:
    def __init__(self,data_validation_config:DataValidationCongif):
        self.data_validation_config=data_validation_config
        

    def data_validation(self)-> bool :
        logging.info("Entered the data_validatin method of DataValidation class")
        try:    
            df = pd.read_csv(self.data_validation_config.DataPath)
            columns = df.columns.tolist()
            
            logging.info(f"the columns in the data file {columns}")
            
            logging.info("Exited the data_validatin method of DataValidation class")

            return set(columns)==set(self.data_validation_config.LABELS)
        
        except Exception as e:
            raise CustomException(e,sys) from e

        
        

        