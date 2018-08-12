FROM python:3
EXPOSE 8080:8080
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install build-essential libmysqlclient-dev python3-dev -y
WORKDIR /src
COPY ./requirements.txt /src/
RUN pip3 install -Ur requirements.txt
COPY . /src
RUN python3 manage.py collectstatic --no-input  CMD ["/bin/bash", "run.sh"]