FROM centos:7
LABEL maintainer "Demetrius Bell <meetri@gmail.com>"

RUN yum install -y gcc epel-release \
&& yum install -y python-pip python-devel \
&& pip install --upgrade pip \
&& pip install flask pyephem pytz egenix-mx-base argparse tzlocal elasticsearch certifi

COPY app /opt/alexa/app/

WORKDIR /opt/alexa/app

ENTRYPOINT ["/opt/alexa/app/run"]
