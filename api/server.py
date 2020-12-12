import json
import requests
import os
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from numpy import expand_dims
from flask import Flask, request, make_response
from flask_restful import Api, Resource, abort
from flask_cors import CORS

UPLOAD_PATH = os.getenv("UPLOAD_PATH")
TF_SERVE_URL = os.getenv("TF_SERVE_URL")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

idg = ImageDataGenerator(
        samplewise_center=True,
        samplewise_std_normalization=True,
        fill_mode='constant',
        cval=1.0)


def allowed_file(filename):
    return '.' in filename \
           and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
CORS(app)
api = Api(app)


def load_img_as_tensor(filepath):
    img = load_img(filepath, target_size=(256, 256), color_mode="rgb")
    img = img_to_array(img)
    tensor = expand_dims(img, axis=0)
    tensor = idg.flow(tensor)
    return next(tensor)


def make_predictions(img):
    labelled_predictions = get_label_prediction(img)
    return {"labels": labelled_predictions}


def get_label_prediction(tensor):
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
              "effusion", "emphysema", "fibrosis", "infiltration",
              "mass", "no_finding", "nodule", "pleural_thickening",
              "pneumothorax"]

    labelled_predictions = []
    for label, prediction in zip(labels, predictions):
        labelled_predictions.append({"label": label, "probability": prediction})

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
        image = load_img_as_tensor(filepath)
        predictions = make_predictions(image)

        os.remove(filepath)

        return predictions, 200


api.add_resource(Predictor, "/")

if __name__ == "__main__":
    HOST_IP = "127.0.0.1" if os.getenv("LOCAL_HOST") == "true" else "0.0.0.0"
    DEBUG_MODE = os.getenv("DEBUG_MODE") == "true"
    app.run(debug=DEBUG_MODE, host=HOST_IP)
