FROM python:3.12.4-slim

WORKDIR /test-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENV flask_app = app.py
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]