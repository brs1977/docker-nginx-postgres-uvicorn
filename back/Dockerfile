FROM python:3.9.15-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir --upgrade pip && \ 
    pip3 install --no-cache-dir -r requirements.txt

COPY . /app

# CMD ["gunicorn", "-b", "0.0.0.0:8015", "--workers", "2", "app:server"]