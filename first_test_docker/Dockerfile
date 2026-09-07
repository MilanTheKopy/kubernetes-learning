FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY docker_test_main.py /app/

CMD ["python", "docker_test_main.py"]