FROM ubuntu:16.04

RUN apt-get update && \
      apt-get -y install sudo

RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

USER docker

RUN git clone https://github.com/ipop-project/Network-Visualizer.git

RUN cd Network-Visualizer/setup

RUN ./setup.sh

EXPOSE 5000

RUN cd ..

CMD ./visualizer start
