import pytest
from pathlib import Path

from flask import Flask
from api.flask_app import app


test_resources = Path(__file__).parent / "test_resources"


@pytest.fixture()
def client():
    return app.test_client()


def test_ocr(client):
    image_file = test_resources / "48.png"
    image_data = image_file.open('rb')

    res = client.post("ocr", data={
        "model_name": "pyocr.tesseract",
        "language": "Japanese",
        "builder": "word_box",
        "image_data": image_data
    }
    )
    assert res.status_code == 200

    res_json = res.json()
    return
