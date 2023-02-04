from flask import Flask
from src.models import models

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello world Flask"

@app.route("/available_models")
def get_available_models():
    model_names = list(models.keys())
    return model_names


@app.route("/available_language/<model_name>")
def get_available_language(model_name):
    if model_name not in models.keys():
        return "false"
    else:
        ret = models[model_name]["languages"]
        return ret