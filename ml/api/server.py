import json
import requests
import os
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
from numpy import expand_dims
from flask import Flask, request
from flask_restful import Api, Resource, abort
import pickle

# TODO: set model path. Keep in container or get from s3?
PROJECT_DIR = "W:/WGU/C964_Capstone/project/ml"

UPLOAD_FOLDER = f"{PROJECT_DIR}/api/tmp"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[
        1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
api = Api(app)

finding_predictor_path = "models/20201124-155102-100-binary-kmeans.pkl"
finding_predictor_path = os.path.join(PROJECT_DIR, finding_predictor_path)


def load_finding_model():
    with open(finding_predictor_path, "rb") as f:
        f_predictor = pickle.load(f)
    return f_predictor


finding_predictor = load_finding_model()


def load_img_as_array(filepath):
    img = load_img(filepath, target_size=(256, 256), color_mode="grayscale")
    img = img_to_array(img)
    return img


def make_predictions(img):
    finding_label = get_finding_prediction(img)
    labelled_predictions = get_label_prediction(img)
    return {"Finding": finding_label, "Label": labelled_predictions}


def get_finding_prediction(img):
    img = img.flatten()
    img = img.reshape(1, -1)

    finding_prediction = finding_predictor.predict(img)
    finding_prediction = finding_prediction[0]

    # if prediction is 0, then there is a finding
    # this also converts the numpy object into a Python boolean which can be
    # serialized
    return True if finding_prediction < 0.5 else False


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

    def post(self):
        if "image" not in request.files:
            abort(400, message="No file present.")

        image = request.files["image"]
        if image and allowed_file(image.filename):
            image.save(os.path.join(UPLOAD_FOLDER, image.filename))
        else:
            abort(400,
                  message=f"Image filetype must be in {ALLOWED_EXTENSIONS}")

        filepath = f"{UPLOAD_FOLDER}/{image.filename}"
        image = load_img_as_array(filepath)
        predictions = make_predictions(image)

        os.remove(filepath)

        return predictions, 200


api.add_resource(Predictor, "/predict")

if __name__ == "__main__":
    app.run(debug=True)
