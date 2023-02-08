"""_summary_

Returns:
    _type_: _description_
"""
import json
from flask import make_response, Response


def create_result(result: any, status: int, message: str = "") -> Response:
    """_summary_

    Args:
        result (any): _description_
        status (int, optional): _description_.
        message (str, optional): _description_. Defaults to "".

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


def format_ocr_results(ocr_results, builder_type) -> dict:
    """
    builderごとに出力内容が変わることがあるのでここでJSONにできるように吸収する
    一旦はword_box,line_boxの場合のみ実装
    

    Args:
        ocr_results (_type_): _description_
        builder (_type_): _description_

    Returns:
        dict: _description_
    """
    if builder_type not in ["word_box", "line_box"]:
        NotImplementedError("Only word_box and line_box are implemented.")


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
