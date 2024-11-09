FROM python:3.12.4

WORKDIR /test-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENV flask_app = app.py
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]