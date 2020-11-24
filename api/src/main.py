from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
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
BUCKET_NAME = "xray.scgrk.com"

# TODO: set model path. Keep in container or get from s3?
finding_predictor_path = "..."
label_classifier_path = "..."

labels = ["atelectasis", "cardiomegaly", "consolidation", "edema", "effusion",
          "emphysema", "fibrosis", "hernia", "infiltration", "mass", "nodule",
          "pleural_thickening", "pneumonia", "pneumothorax"]


def load_models():
    with open(finding_predictor_path, 'rb') as f:
        f_predictor = pickle.load(f)
    l_classifier = load_model(label_classifier_path)
    return f_predictor, l_classifier


finding_predictor, label_classifier = load_models()


class Bucket(Resource):
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
    # TODO: This will (probably?) not work without making the bucket public
    #  Lazy solution is to make gets public.
    #  Easy/inefficient is to get presigned url
    #  Correct is to use the s3 client, download it locally (if unable to load
    #   directly from memory), then load from the saved file
    filepath = f"https://s3.amazonaws.com/{BUCKET_NAME}/{filename}"
    img = load_img(filepath, target_size=(256, 256), color_mode='grayscale')
    img = img_to_array(img)
    return img


def make_predictions(img):
    finding_prediction = finding_predictor.predict(img.flatten())
    tensor = expand_dims(img, axis=0)
    label_prediction = label_classifier.predict(tensor)
    # TODO: Need to figure out the labels associated with each array index
    return {"Finding": finding_prediction, "Label": label_prediction}


class Predictor(Resource):

    def get(self, filename):
        img = load_img_as_array(filename)
        predictions = make_predictions(img)
        return predictions


api.add_resource(Bucket, "/upload")
api.add_resource(Predictor, "/predict/<filename>")

if __name__ == "__main__":
    app.run(debug=True)
