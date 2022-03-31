
FROM ubuntu:trusty
RUN sudo apt-get -y update
RUN sudo apt-get -y upgrade
RUN sudo apt-get install -y sqlite3 libsqlite3-dev
#RUN mkdir db
#RUN /usr/bin/sqlite3 /db/ashop.db
#CMD /bin/bash


WORKDIR /myshop

FROM python:3.8


COPY requerements.txt .

RUN pip install -r requerements.txt



#COPY APP FROM FOLDER TO CONTAINER FOLDER
COPY ./app ./app
COPY ./static ./static
COPY ./templates ./templates


CMD ["python", "./app/main.py"]

#BUILD APP
# sudo docker build -t awebapp .
# TO RUN IT DEFINE PORT (MAPIT) INSIDE/OUT
# sudo docker run -p 8001:8001 awebapp

#docker run -it -v /home/dbfolder/:/db imagename
