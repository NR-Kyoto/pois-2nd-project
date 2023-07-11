FROM python:3.10
USER root

RUN apt-get update
RUN apt-get -y install locales && localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get -y install nodejs
RUN apt-get -y install npm
RUN npm install -g yarn
# RUN yarn install
WORKDIR /root/templats
RUN yarn install
# RUN yarn run dev

WORKDIR /root

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

COPY requirements.txt /root/

RUN apt-get install -y fonts-noto-cjk

RUN apt-get install -y vim less
RUN apt-get install -y flac
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN pip install -r /root/requirements.txt