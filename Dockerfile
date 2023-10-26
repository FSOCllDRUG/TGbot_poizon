FROM python:3.11-slim-buster

WORKDIR /app_main

COPY . /app_main

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run.py"]