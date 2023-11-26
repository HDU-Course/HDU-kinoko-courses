FROM ubuntu:latest

RUN apt-get update && apt-get install -y iptables

COPY ./iptables.rules /etc/iptables.rules

CMD ["/bin/bash"]