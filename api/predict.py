import boto3
import tensorflow as tf

s3_client = boto3.client("s3")

bucket = 'xray.scgrk.com'
model_key = '20201119152723_InceptionV3.h5'
bin_model = s3_client.download_file(bucket, model_key, f'/tmp/{model_key}')
model = tf.keras.models.load_model(f'/tmp/{model_key}')


def handler(event, context):
    # not sure if this is the right property
    tensor = convert_to_tensor(event.body)
    prediction = model.predict(tensor)
    return prediction


def convert_to_tensor(payload):
    pass
