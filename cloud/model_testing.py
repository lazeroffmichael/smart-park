from google.api_core.client_options import ClientOptions
from googleapiclient import discovery
import os
from sklearn.preprocessing import MinMaxScaler
import joblib
import tensorflow as tf
import pandas as pd

ENDPOINT = f"https://{os.getenv('REGION')}-ml.googleapis.com"
CLIENT_OPTIONS = ClientOptions(api_endpoint=ENDPOINT)
ML = discovery.build('ml', 'v1', client_options=CLIENT_OPTIONS)
SCALER = joblib.load('../model/scaler.gz')

scaler = MinMaxScaler()
test_data_enter = [[36.11128658900951, -115.1407443542069, 36.11138568488752, -115.1407532525297, 36.11145950467051,
             -115.1407476558897, 36.11157110102095, -115.1407108213047]]
transformed_data = SCALER.transform(test_data_enter)

request_body = {
    'instances': transformed_data.tolist()
}
name=f"projects/{os.getenv('projectId')}/models/{os.getenv('MODEL_NAME')}/versions/{os.getenv('VERSION_NAME')}"
request = ML.projects().predict(
    name=name,
    body=request_body
)
response = request.execute()
for item in response['predictions']:
    if item[0] > 0.5:
        print(1)
    else:
        print(0)
