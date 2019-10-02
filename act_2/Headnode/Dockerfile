# Same thing than the 'server' Dockerfile.
#FROM python:latest

# Same thing than the 'server' Dockerfile.
# We import 'client.py' in '/client/' folder.
#ADD headnode.py /Headnode/

# I would like to introduce something new, the 'WORKDIR' command.
# This command changes the base directory of your image.
# Here we define '/client/' as base directory.
#WORKDIR /Headnode/

FROM ubuntu:latest

RUN apt-get update \
	&& apt-get -y install python3 \
	&& apt-get -y install python3-pip \
	&& apt-get -y install nano

ADD headnode.py /Headnode/

WORKDIR /Headnode/
