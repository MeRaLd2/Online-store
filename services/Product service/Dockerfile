FROM python:3.11

RUN direct /product-service

WORKDIR /product-service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]