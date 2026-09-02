FROM python:3.12-slim

WORKDIR /app

# Install SUMO and required system tools
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       sumo \
       sumo-tools \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY sumo ./sumo
COPY tests ./tests

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]