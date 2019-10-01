FROM ubuntu:latest

RUN apt-get update \
	&& apt-get -y install iputils-ping \
	&& apt-get -y install iproute2 \
	&& apt-get -y install dnsutils \
	&& apt-get -y install python3 \
	&& apt-get -y install python3-pip \
	&& apt-get -y install nano


ADD client.py /cliente/

WORKDIR /cliente
