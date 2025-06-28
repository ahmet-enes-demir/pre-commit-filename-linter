FROM python:3.13.5-alpine3.22

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY setup.py .

RUN pip3 install -e .

ENTRYPOINT ["python3"]
