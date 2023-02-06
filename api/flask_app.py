"""_summary_

Returns:
    _type_: _description_
"""
import json
from PIL import Image
from flask import Flask, request, make_response, Response, jsonify

from src.models import models, builders

app = Flask(__name__)


def create_result(result: any, message: str = "", status: int = 500) -> Response:
    """_summary_

    Args:
        result (bool): _description_

    Returns:
        Response: _description_
    """

    try:
        ret = {
            "result": result,
            "message": message
        }
        response = make_response(json.dumps(ret), status)
    except Exception as ex:
        response = make_response(json.dumps(
            {"result": False, "message": f"{ex}"}), 400)
    else:
        return response


@app.route("/")
def hello() -> Response:
    """_summary_

    Returns:
        Response: _description_
    """
    return create_result(result=True, message="this_is_pyocr_api")


@app.route("/available_models", methods=["GET"])
def get_available_models() -> Response:
    """ Return of available model names

    Returns:
        Response: List[str] Names of the available models
    """
    model_names = list(models.keys())
    return create_result(result=model_names)


@app.route("/available_language/<model_name>", methods=["GET"])
def get_available_language(model_name: str) -> Response:
    """ Return of available languages for which the selected model is in use

    Args:
        model_name (str): model name

    Returns:
        Response: List[str] Names of the available languages
    """
    if model_name not in models.keys():
        return create_result(
            result=False,
            message="No language available for the selected model.",
            status=200
        )
    else:
        ret = models[model_name]["languages"]
        return create_result(
            result=ret,
            status=200
        )


@app.route("/ocr", methods=["POST"])
def ocr() -> Response:
    """_summary_
    """
    # get parameters
    try:
        req_model_name = request.form['model_name']
        req_language = request.form['language']
        req_builder = request.form['builder']
    except KeyError as ex:
        return create_result(result=False, message=f"Lack of required parameters.: {ex}", status=400)

    # validate parameters
    if not req_model_name:
        return create_result(result=False, message="empty model_name", status=422)
    if not req_model_name in models.keys():
        return create_result(result=False, message="unavailable model_name", status=422)

    if not req_language:
        return create_result(result=False, message="empty language", status=422)
    if not req_language in models[req_model_name]["languages"]:
        return create_result(result=False, message="unavailable language", status=422)

    if not req_builder:
        return create_result(result=False, message="empty builder", status=422)
    if not req_builder in builders.keys():
        return create_result(result=False, message="unavailable builder", status=422)

    parameters = {
        "model_name": req_model_name,
        "language": req_language,
        "builder": req_builder
    },

    # get images
    try:
        src_image = request.files["image_data"]
    except KeyError as ex:
        return create_result(result=False, message=f"Lack of required image files.: {ex}", status=400)

    # validate images
    # change image formats
    if src_image.content_type == "image/png":
        # if req_model_name == "pyocr.lbtesseract":
        #     validated_src_image = Image.open(io.BytesIO(src_image))

        validated_src_image = Image.open(src_image)
    elif src_image.content_type == "image/jpg":
        validated_src_image = Image.open(src_image)
    else:
        return create_result(result=False, message=f"unavailable image file format.: {ex}", status=400)

    model = models[req_model_name]["tool"]
    builder = builders[req_builder]

    # ocr

    try:
        ocr_results = model.image_to_string(
            image=validated_src_image,
            lang=req_language,
            builder=builder
        )
    except Exception as ex:
        return create_result(result=False, message=f"OCR process error: {ex}", status=500)

    def format_ocr_results(ocr_results, builder) -> dict:
        contents = ""
        boxes = []
        for item in ocr_results:
            contents += item.content
            boxes.append(
                {
                    "content": item.content,
                    "posistion" : item.position
                }
            )

        return {
            "contents" : contents,
            "boxes" : boxes
        }

    # format OCR results
    try:
        formatted_results = format_ocr_results(ocr_results, builder)
    except NotImplementedError as ex:
        return create_result(result=False, message=f"{ex}", status=422)

    return create_result(
        result=formatted_results,
        message=parameters,
        status=200
    )
