from flask import Flask, request
import pandas as pd
import pickle
import os
from flask_restx import Api, Resource, fields



EXCPECTED_COLUMNS = ["gestation","parity","age","height","weight","smoke"]


app = Flask(__name__)

# configure your swagger UI
api = Api(app, title="Flask API Documentation", description="Test your APIs here", doc="/docs")


# create namespace
hello_ns = api.namespace("Hello", description="Hello APIs", path="/hello")
user_ns = api.namespace("User", description="User CRUD operations", path="/user")
pred_ns = api.namespace("Prediction", description="Prediction operations", path="/predict")




# create class for your namespace
@hello_ns.route('/')
class Hello(Resource):
    def get(self):
        return {"msg":"Hello World!"} 




# CRUD operations for user application
@user_ns.route('/')
class User(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass




input_model = pred_ns.model("PredictionInput",{
                        "gestation":fields.List(fields.Float, required=True),
                        "parity":fields.List(fields.Integer, required=True),
                        "age":fields.List(fields.Float, required=True),
                        "height":fields.List(fields.Float, required=True),
                        "weight":fields.List(fields.Float, required=True),
                        "smoke": fields.List(fields.Float, required=True)
                        })



## prediction API docs
@pred_ns.route('/')
class Prediction(Resource):
    @pred_ns.expect(input_model)
    def post(self):
        """
            Predicts the baby's birth weight based on input parameters.

            **Request Body Format:**
            - `gestation` (List[int]): Number of gestation days
            - `parity` (List[int]): Parity value
            - `age` (List[int]): Mother's age
            - `height` (List[int]): Mother's height
            - `weight` (List[int]): Mother's weight
            - `smoke` (List[int]): Smoking status (0 or 1)

            **Returns:**
            - JSON response containing predicted outcome as a float.
        """

        baby_data_form = request.get_json()

        # convert into dataframe
        baby_df = pd.DataFrame(baby_data_form)
        baby_df = baby_df[EXCPECTED_COLUMNS]

        # load machine leanring trained model
        path = os.path.join(os.path.dirname(__file__), "model.pkl")
        with open(path, 'rb') as obj:
            model = pickle.load(obj)

        # make prediciton on user data
        prediction = model.predict(baby_df)
        prediction = round(float(prediction), 2)

        # return reponse in a json format
        response = {"Prediction":prediction}
        return response







def get_cleaned_data(form_data):
    gestation = float(form_data['gestation'])
    parity = int(form_data['parity'])
    age = float(form_data['age'])
    height = float(form_data['height'])
    weight = float(form_data['weight'])
    smoke = float(form_data['smoke'])

    cleaned_data = {"gestation":[gestation],
                    "parity":[parity],
                    "age":[age],
                    "height":[height],
                    "weight":[weight],
                    "smoke":[smoke]
                    }

    return cleaned_data


@app.route("/hello", methods=['GET'])
def hello():
    return {"msg":"Hello World!"}







# predict endpoint
@app.route("/predict", methods = ['POST'])
def get_prediction():
    baby_data_form = request.get_json()

    # convert into dataframe
    baby_df = pd.DataFrame(baby_data_form)
    baby_df = baby_df[EXCPECTED_COLUMNS]

    # load machine leanring trained model
    path = os.path.join(os.path.dirname(__file__), "model.pkl")
    with open(path, 'rb') as obj:
        model = pickle.load(obj)

    # make prediciton on user data
    prediction = model.predict(baby_df)
    prediction = round(float(prediction), 2)

    # return reponse in a json format
    response = {"Prediction":prediction}
    return response





if __name__=='__main__':
    app.run(debug=True)




