import numpy as np
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")
import tensorflow as tf
from tensorflow import keras
import random
# Load the model
lstm_model = keras.models.load_model('api/Model/LSTM_model.h5')
# ARF model
# json_data = json.load(fp=open("/Users/as/TanuProjects/amex_project/testing_data.json"))
'''import pickle
with open('api/Model/ARF_evaluator.pkl','rb') as file:
    arf_evaluator=pickle.load(file)'''

def lstm_predictions(df):
    features = np.array(df)
    features_reshaped = features.reshape(features.shape[0], 1, features.shape[1])
    lstm_y_pred=lstm_model.predict(features_reshaped)
    lstm_y_pred_binary = (lstm_y_pred > 0.5).astype(int)
    print(lstm_y_pred_binary)
    return lstm_y_pred_binary

'''def arf_pred(df):
    data = np.array(df)
    arf_pred=arf_evaluator.predict(data)
    arf_predictions=np.array(arf_pred[0])
    arf_predtn= np.reshape(arf_predictions,(-1,1))
    print(arf_predtn)
    return arf_predtn'''

def combined_predctns(df):
    lstm_predtns=lstm_predictions(df)
   # arf_predtns=arf_pred(df)
    lstm_weight= 0.6
    #arf_weight=0.4
    #combined_predictions= ((lstm_weight * lstm_predtns + arf_weight * arf_predtns)/(lstm_weight+arf_weight))
    #print(combined_predictions)
    combined_predictions = (lstm_predtns > 0.5).astype(int)
    return combined_predictions

