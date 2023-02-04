import pyocr
import pyocr.builders

models = {}

tools = pyocr.get_available_tools()

for tool in tools:
    models[tool.__name__] = {
        "languages": tool.get_available_languages(),
        "tool": tool
        }