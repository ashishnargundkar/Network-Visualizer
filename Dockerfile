FROM ubuntu:16.04

COPY ./badproxy /etc/apt/apt.conf.d/99fixbadproxy

ENV VIS_DIR ~/Network-Visualizer

RUN apt-get update -y

RUN apt-get -y install apt-utils apt-transport-https git curl python3 python3-setuptools python3-dev python3-pip mongodb nodejs

RUN git clone --single-branch -b docker-support https://github.com/ashishnargundkar/Network-Visualizer.git $VIS_DIR

RUN $VIS_DIR/setup.sh

EXPOSE 5000

CMD $VIS_DIR/visualizer start
