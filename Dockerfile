FROM ubuntu:16.04

ENV VIS_DIR ~/Network-Visualizer

RUN apt-get update -y

RUN apt-get -y install apt-utils

RUN apt-get update -y

RUN apt-get -y install apt-transport-https

RUN apt-get update -y

RUN apt-get update -y

RUN apt-get install -y git

RUN apt-get update -y

RUN git clone --single-branch -b docker-support https://github.com/ipop-project/Network-Visualizer.git $VIS_DIR && cd $VIS_DIR/setup && ./setup.sh

EXPOSE 5000

CMD $VIS_DIR/visualizer start
