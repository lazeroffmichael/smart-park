from google.api_core.client_options import ClientOptions
from googleapiclient import discovery
import os
from sklearn.preprocessing import MinMaxScaler

ENDPOINT = f"https://{os.getenv('REGION')}-ml.googleapis.com"
CLIENT_OPTIONS = ClientOptions(api_endpoint=ENDPOINT)
ML = discovery.build('ml', 'v1', client_options=CLIENT_OPTIONS)


def test_example():
    scaler = MinMaxScaler()
    test_data = [36.11128658900951, -115.1407443542069, 36.11138568488752, -115.1407532525297, 36.11145950467051,
                 -115.1407476558897, 36.11157110102095, -115.1407108213047]
    transformed_data = scaler.fit_transform(test_data)
    request_body = {
        'instances': transformed_data
    }
    request = ML.projects().predict(
        name=f"projects/{os.getenv('projectId')}/models/{os.getenv('MODEL_NAME')}/{os.getenv('VERSION_NAME')}",
        body=request_body
    )
    response = request.execute()
    print(response)
