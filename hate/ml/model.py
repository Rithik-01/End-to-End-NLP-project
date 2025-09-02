from hate.entity.config_entity import ModelTrainerConfig
import tensorflow as tf
from keras.models import Sequential
from keras.optimizers import RMSprop
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import LSTM,Activation,Dense,Dropout,Input,Embedding,SpatialDropout1D
from hate.constants import *

class ModelArchitecture:

    def __init__(self, vectorizer):
        self.vectorizer = vectorizer

    
    def get_model(self):
        model = Sequential()
        model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
        model.add(self.vectorizer)
        model.add(Embedding(MAX_WORDS, 100,input_length=MAX_LEN))
        model.add(SpatialDropout1D(0.2))
        model.add(LSTM(100,dropout=0.2,recurrent_dropout=0.2))
        model.add(Dense(1,activation=ACTIVATION))
        model.summary()
        model.compile(loss=LOSS,optimizer=RMSprop(),metrics=METRICS)

        return model