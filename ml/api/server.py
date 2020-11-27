import json
import requests
import os
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
from numpy import expand_dims
from flask import Flask, request, make_response
from flask_restful import Api, Resource, abort
from flask_cors import CORS
import pickle

UPLOAD_PATH = os.getenv("UPLOAD_PATH")
MODEL_PATH = os.getenv("MODEL_PATH")
TF_SERVE_URL = os.getenv("TF_SERVE_URL")
HOST_IP = "127.0.0.1" if os.getenv("LOCAL_HOST") else "0.0.0.0"
DEBUG_MODE = os.getenv("DEBUG_MODE")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return '.' in filename \
           and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
CORS(app)
api = Api(app)


def load_finding_model():
    with open(MODEL_PATH, "rb") as f:
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

    response = requests.post(TF_SERVE_URL, data=classifier_request)
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

    def options(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

    def get(self):
        # Used for testing server is up and responding.
        return "Use POST for predictions.", 200

    def post(self):
        rec = request
        print(rec)
        if "image" not in request.files:
            abort(400, message="No file present.")

        image = request.files["image"]
        if image and allowed_file(image.filename):
            image.save(os.path.join(UPLOAD_PATH, image.filename))
        else:
            abort(400,
                  message=f"Image filetype must be in {ALLOWED_EXTENSIONS}")

        filepath = f"{UPLOAD_PATH}/{image.filename}"
        image = load_img_as_array(filepath)
        predictions = make_predictions(image)

        os.remove(filepath)

        return predictions, 200


api.add_resource(Predictor, "/")

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, host=HOST_IP)
