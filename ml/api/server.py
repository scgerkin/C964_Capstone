import json
import requests
import os
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
from numpy import expand_dims
from flask import Flask
from flask_restful import Api, Resource, abort
import boto3
from botocore.exceptions import ClientError
import uuid
import pickle

app = Flask(__name__)
api = Api(app)

# todo: get bucket name from environ or config file
# todo: add bucket policy to automatically delete after set time
BUCKET_NAME = "scgrk.com"

# TODO: set model path. Keep in container or get from s3?
PROJECT_DIR = "W:/WGU/C964_Capstone/project/ml/"

finding_predictor_path = "models/20201124-155102-100-binary-kmeans.pkl"
finding_predictor_path = os.path.join(PROJECT_DIR, finding_predictor_path)


def load_finding_model():
    with open(finding_predictor_path, 'rb') as f:
        f_predictor = pickle.load(f)
    return f_predictor


finding_predictor = load_finding_model()


class Bucket(Resource):
    """
    FIXME: I think I might replace this with just posting the image directly
        to the server, saving it in a temp folder, and processing it from
        that rather than deal with S3. Since `load_img` can't load from a web
        URL file path, putting it onto S3 is just an extra step that adds no
        benefit.
    """
    s3 = boto3.client("s3")

    expiration = 600  # 10 minutes

    def get(self):
        key_name = str(uuid.uuid4())
        try:
            res = self.s3.generate_presigned_post(BUCKET_NAME,
                                                  key_name,
                                                  ExpiresIn=self.expiration)
            return res, 200
        except ClientError as ex:
            # todo: log exception, don't return the exception code
            print(ex)
            abort(500, message=ex.response)


def load_img_as_array(filename):
    # FIXME: Apparently load_img can't take a web URL
    # filepath = f"https://s3.amazonaws.com/{BUCKET_NAME}/{filename}"
    filepath = "W:/WGU/C964_Capstone/project/ml/dataset/images/00000001_000.png"
    img = load_img(filepath, target_size=(256, 256), color_mode='grayscale')
    img = img_to_array(img)
    return img


def make_predictions(img):
    finding_label = get_finding_prediction(img)
    labelled_predictions = get_label_prediction(img)
    return {"Finding": finding_label, "Label": labelled_predictions}


def get_finding_prediction(img):
    img = img.flatten()
    # FIXME: above is not flattening from 2d to 1d array, so predictor
    #  has a fit
    # finding_prediction = finding_predictor.predict(img)

    finding_prediction = 1
    # if prediction is 0, then there is a finding
    return finding_prediction < 0.5


def get_label_prediction(img):
    tensor = expand_dims(img, axis=0)

    classifier_request = json.dumps({
        "signature_name": "serving_default",
        "instances"     : tensor.tolist()
        })

    server_url = "http://localhost:8501/v1/models/dx-classifier:predict"
    response = requests.post(server_url, data=classifier_request)
    response = response.json()

    predictions = np.array(response["predictions"][0])
    predictions.round(2)
    predictions = predictions.tolist()

    labels = ["atelectasis", "cardiomegaly", "consolidation", "edema",
              "effusion", "emphysema", "fibrosis", "hernia", "infiltration",
              "mass", "nodule", "pleural_thickening", "pneumonia",
              "pneumothorax"]

    labelled_predictions = {}
    for i in range(len(predictions)):
        labelled_predictions[labels[i]] = predictions[i]

    return labelled_predictions


class Predictor(Resource):

    def get(self, filename):
        img = load_img_as_array(filename)
        predictions = make_predictions(img)
        return predictions

    def post(self):
        pass


api.add_resource(Bucket, "/upload")
api.add_resource(Predictor, "/predict/<filename>")

if __name__ == "__main__":
    app.run(debug=True)
