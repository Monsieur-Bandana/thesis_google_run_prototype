FROM python:3.24.3-slim

WORKDIR /test-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY keen-dispatch-385408-7150201568b0.json /app/key.json

COPY . .
ENV flask_app = app.py
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/key.json
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]