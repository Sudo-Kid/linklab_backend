FROM python:3.6

EXPOSE "8000:8000"
EXPOSE "8080:8080"

RUN apt-get update && apt-get upgrade -y
ADD . /src
WORKDIR /src

RUN pip install -r requirements.txt
RUN pip install -U uwsgi
RUN python3 manage.py collectstatic --no-input
RUN python3 manage.py migrate

RUN mkdir media

CMD [ "uwsgi", "--http", "0.0.0.0:8080", \
               "--wsgi-file", "/src/linklab/wsgi.py", \
               "--static-map", "/static=/src/static/"]
