from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)


class Foo(Resource):

    def __init__(self):
        self.data = {"alpha": "bravo", "charlie": "delta"}
        self.put_args = reqparse.RequestParser()
        self.put_args.add_argument("name",
                                   type=str,
                                   help="Help message goes here",
                                   required=True)

    def abort_on_unknown_id(self, id):
        if id not in self.data:
            abort(404, message=f"Unknown ID: {id}")

    def get(self, id):
        self.abort_on_unknown_id(id)
        return self.data[id], 200

    def post(self):
        pass

    def put(self, id):
        args = self.put_args.parse_args()
        self.data[id] = args
        return self.data[id], 201

    def delete(self, id):
        self.abort_on_unknown_id(id)
        del self.data[id]
        return id, 204


api.add_resource(Foo, "/foo/<str:id>")

if __name__ == "__main__":
    app.run(debug=True)
