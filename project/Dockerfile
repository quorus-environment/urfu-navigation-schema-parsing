FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt /app

RUN apt-get update && apt-get install libglib2.0-0 libsm6 libxext6 libgl1  -y
RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . /app

CMD ["gunicorn", "parse_shema.wsgi:application", "--bind", "0.0.0.0:8000" ]
