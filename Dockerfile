FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p data/db && chmod 755 data/db

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]