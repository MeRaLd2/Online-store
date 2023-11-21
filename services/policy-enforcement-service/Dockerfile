FROM python:3.11-slim

WORKDIR /

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./src /src

CMD ["uvicorn", "src:app", "--host", "0.0.0.0", "--port", "5100"]