from tensorflow.keras.models import load_model
from flask import Flask
from flask_restful import Api, Resource, abort
import boto3
from botocore.exceptions import ClientError
import uuid

app = Flask(__name__)
api = Api(app)

# todo: get bucket name from environ or config file
# todo: add bucket policy to automatically delete after set time
BUCKET_NAME = "xray.scgrk.com"

# TODO: set model path. Keep in container or get from s3?
finding_predictor_path = "..."
label_classifier_path = "..."
finding_predictor = load_model(finding_predictor_path)
label_classifier = load_model(label_classifier_path)


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


def load_img_as_tensor(filename):
    filepath = f"https://s3.amazonaws.com/{BUCKET_NAME}/{filename}"
    # load image as tensor and return it
    raise NotImplemented("load image")


def make_predictions(tensor):
    # is this right?
    # predictions = self.model.predict_proba(tensor)
    return {"a": "b"}
    # raise NotImplemented("make predictions")


class Predictor(Resource):

    def get(self, filename):
        tensor = load_img_as_tensor(filename)
        predictions = make_predictions(tensor)
        return predictions


api.add_resource(Bucket, "/upload")
api.add_resource(Predictor, "/predict/<filename>")

if __name__ == "__main__":
    app.run(debug=True)
