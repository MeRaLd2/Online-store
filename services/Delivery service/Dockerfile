FROM python:3.11

WORKDIR /src

COPY requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /src/app

ARG APP_IP
ARG APP_PORT

ENV APP_IP $APP_IP
ENV APP_PORT $APP_PORT

EXPOSE $APP_PORT

CMD ["uvicorn", "app.app:app", "--host", "$APP_IP", "--port", "$APP_PORT"]