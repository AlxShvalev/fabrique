FROM python:3.10-slim

WORKDIR app/

COPY requirements.txt .

RUN apt-get update
RUN apt-get update
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "fabrique.wsgi:application", "--bind", "0:8000" ]
