FROM python:3.6
LABEL MAINTAINER="Dileep Kishore (dkishore@bu.edu)"

ENV APP_DIR /home/microbiome_api
RUN mkdir -p $APP_DIR
WORKDIR $APP_DIR

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "microbiome_api.app:create_app()"