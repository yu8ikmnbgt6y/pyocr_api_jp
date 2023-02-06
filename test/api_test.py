"""_summary_

Returns:
    _type_: _description_
"""
from pathlib import Path

import pytest
from api.flask_app import app


test_resources = Path(__file__).parent / "test_resources"


@pytest.fixture()
def client():
    return app.test_client()

    # "text": pyocr.builders.TextBuilder(),
    # "word_box": pyocr.builders.WordBoxBuilder(),
    # "line_box": pyocr.builders.LineBoxBuilder(),
    # "digit": pyocr.builders.DigitBuilder()


test_images = [
    "1.jpg",
    "2.png",
    "3.png"
]
test_images = [test_resources / x for x in test_images]
model_names = ["pyocr.tesseract", "pyocr.libtesseract"]

@pytest.mark.parametrize("model_name", model_names)
@pytest.mark.parametrize("test_image", test_images)
def test_ocr(client, test_image, model_name):
    image_file = test_image
    image_data = image_file.open('rb')

    res = client.post("ocr", data={
        "model_name": model_name,
        "language": "Japanese",
        "builder": "word_box",
        "image_data": image_data
    }
    )
    assert res.status_code == 200
    res_json = res.json
    return
