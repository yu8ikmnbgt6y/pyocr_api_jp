FROM python:3.10.9-bullseye

WORKDIR /work

RUN apt update && apt -y upgrade
RUN apt -y install tesseract-ocr tesseract-ocr-jpn libtesseract-dev libleptonica-dev tesseract-ocr-script-jpan tesseract-ocr-script-jpan-vert 

COPY requirements.txt .

RUN pip install -U pip && pip install -r requirements.txt

COPY main.py launch.sh ./
COPY src/ ./src/
COPY api/ ./api/

CMD ["/bin/sh", "launch.sh"]