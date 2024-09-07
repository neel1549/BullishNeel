
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["python", "main_crypto.py"]