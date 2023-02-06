"""_summary_
"""
from typing import Dict
from pyocr.builders import BaseBuilder

import pyocr
import pyocr.builders

models: Dict[str, any] = {} # [str, module]

tools = pyocr.get_available_tools()

for tool in tools:
    models[tool.__name__] = {
        "languages": tool.get_available_languages(),
        "tool": tool
        }

builders : Dict[str, BaseBuilder]= {
    "text": pyocr.builders.TextBuilder(),
    "word_box": pyocr.builders.WordBoxBuilder(),
    "line_box": pyocr.builders.LineBoxBuilder(),
    "digit": pyocr.builders.DigitBuilder()
}
