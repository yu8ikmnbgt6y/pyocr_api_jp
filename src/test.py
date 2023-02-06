from PIL import Image, ImageDraw

import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()

if len(tools) == 0:
    print("no tools")
    raise SystemError()
    exit()

print("available_tools: ", ",".join([x.get_name() for x in tools]))
tool = tools[1]


langs = tool.get_available_languages()
if len(langs) == 0:
    print("no langs")
    raise SystemError()
    exit()

print("available_langages: ", ",".join(langs))
# tgt_lang  = langs[0]
tgt_lang = "Japanese_vert"

pyocr_txt_builder = pyocr.builders.TextBuilder()
pyocr_wb_builder = pyocr.builders.WordBoxBuilder()
pyocr_lb_builder = pyocr.builders.LineBoxBuilder()
pyocr_dg_builder = pyocr.builders.DigitBuilder()


srcImg = Image.open('801496_R0000055.jpg')
dstImg = Image.open('801496_R0000055.jpg')
draw = ImageDraw.Draw(dstImg)


txt = tool.image_to_string(
    srcImg,
    lang=tgt_lang,
    builder=pyocr_txt_builder
)
print(txt)


wbs = tool.image_to_string(
    srcImg,
    lang=tgt_lang,
    builder=pyocr_wb_builder
)
for wb in wbs:
    print(wb.content)
    draw.rectangle(wb.position, outline=(255,0,0), width=2)

lbs = tool.image_to_string(
    srcImg,
    lang=tgt_lang,
    builder=pyocr_lb_builder
)

for lb in lbs:
    print(lb.content)
    draw.rectangle(lb.position, outline=(0,0,255), width=2)


digits = tool.image_to_string(
    srcImg,
    lang=tgt_lang,
    builder=pyocr_dg_builder
)
print(digits)


dstImg.save("dst.png")