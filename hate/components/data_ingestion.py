import os 
import sys 
from zipfile import ZipFile
from hate.logger import logging
from hate.exceptional import CustomException
from hate.configuration.gcloud_syncer import GCloudSync
from hate.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config=data_ingestion_config
        self.gcloud=GCloudSync()

    def get_data_from_gcloud(self) -> None:
        try:
            logging.info("Entered the get_data_from_gcloud method of Data ingestion class")
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACT_DTR,exist_ok=True)

            self.gcloud.sync_folder_from_gcloud(self.data_ingestion_config.BUCKET_NAME,
                                                self.data_ingestion_config.ZIP_FILE_NAME,
                                                self.data_ingestion_config.DATA_INGESTION_ARTIFACT_DIR,)
            
            logging.info("Exited the get_data_from_gcloud method of data ingestion class")

        except Exception as e:
            raise CustomException(e,sys) from e

     