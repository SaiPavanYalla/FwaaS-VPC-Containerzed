FROM ubuntu:20.04


RUN apt-get update
RUN apt-get -y --force-yes install iproute2
RUN apt-get -y --force-yes install net-tools
RUN apt-get -y --force-yes install openssh-server
RUN apt-get -y --force-yes install ansible
RUN apt-get -y --force-yes install iptables
RUN apt-get -y --force-yes install iputils-ping
RUN apt-get -y --force-yes install traceroute
RUN apt-get -y --force-yes install tcpdump
RUN apt-get -y --force-yes install iperf
RUN apt-get -y --force-yes install vim
RUN apt-get -y --force-yes install python3
RUN apt-get -y --force-yes install keepalived
RUN apt-get -y --force-yes install python-pexpect
RUN apt-get -y --force-yes install nano

RUN mv /usr/sbin/tcpdump /usr/bin/tcpdump
RUN ln -s /usr/bin/tcpdump /usr/sbin/tcpdump \
&& rm -rf /var/lib/apt/lists/*

RUN /sbin/sysctl -w net.ipv4.conf.all.forwarding=1
# Set the working directory
WORKDIR /home

RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
# Expose any required ports (optional, based on your use case)
EXPOSE 22 80 443



CMD ["bash"]

