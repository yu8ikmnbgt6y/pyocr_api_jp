"""_summary_

Returns:
    _type_: _description_
"""
import json
from flask import make_response, Response


def create_result(result: any, message: str = "", status: int = 500) -> Response:
    """_summary_

    Args:
        result (any): _description_
        message (str, optional): _description_. Defaults to "".
        status (int, optional): _description_. Defaults to 500.

    Returns:
        Response: _description_
    """
    try:
        ret = {
            "result": result,
            "message": message
        }
        response = make_response(
            json.dumps(ret),
            status
        )
        response.mimetype = 'application/json'
    except Exception as ex:
        response = make_response(
            json.dumps({"result": False, "message": f"{ex}"})
            , 400
        )
        response.mimetype = 'application/json'
        return response
    else:
        return response


def format_ocr_results(ocr_results, builder) -> dict:
    """_summary_

    Args:
        ocr_results (_type_): _description_
        builder (_type_): _description_

    Returns:
        dict: _description_
    """
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
