FROM python:3.12.4-slim

# Copy service account key
COPY ../keen-dispatch-385408-7150201568b0.json /app/key.json

# Set environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/key.json

WORKDIR /load-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Specify the command to run your application
CMD ["python", "llm_loader_into_gcrs.py"]