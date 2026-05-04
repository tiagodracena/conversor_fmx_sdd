FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY convert.py app.py ./
COPY templates/ templates/

RUN mkdir -p /tmp/converter/uploads /tmp/converter/outputs

EXPOSE 5000

CMD ["python", "app.py"]