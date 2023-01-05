FROM python:3.10.9-slim

WORKDIR /app

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1 
# Prevents Python from buffering stdout and stderr 
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app

RUN pip install --no-cache-dir --upgrade pip && \ 
    pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# COPY . /app
# CMD ["gunicorn", "-b", "0.0.0.0:8015", "--workers", "2", "app:server"]