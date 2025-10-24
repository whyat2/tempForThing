FROM python:3.14.0-alpine3.22

WORKDIR /app

RUN apk add --no-cache build-base mariadb-dev

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# "app:app" = app.py file and Flask app instance named 'app'
CMD ["python", "goodRequests.py"]