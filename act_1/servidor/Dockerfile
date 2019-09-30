FROM ubuntu:latest 

RUN apt-get update \
	&& apt-get -y install iputils-ping \
	&& apt-get -y install iproute2 \
	&& apt-get -y install dnsutils \
	&& apt-get -y install python3 \
	&& apt-get -y install python3-pip \
	&& apt-get -y install nano

WORKDIR /server

COPY . ./

RUN chmod +x ./run_server.sh

ENTRYPOINT ./run_server.sh