FROM python:3.11.4-slim-bullseye

WORKDIR /app

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY producer.py .

# CMD ["python", "producer.py"]
CMD ["sh", "-c", "sleep 30 && python producer.py"]