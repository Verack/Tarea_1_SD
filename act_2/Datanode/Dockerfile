
#FROM python:latest

#ADD datanode.py /Datanode/ 


#WORKDIR /Datanode/

FROM ubuntu:latest

RUN apt-get update \
	&& apt-get -y install python3 \
	&& apt-get -y install python3-pip \
	&& apt-get -y install nano

ADD datanode.py /Datanode/

WORKDIR /Datanode/