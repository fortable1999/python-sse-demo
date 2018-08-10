FROM node:10

ENV HOME=/home/app

USER app
RUN mkdir $HOME/nodeapp # directories created by WORKDIR belong to root
WORKDIR $HOME/nodeapp

COPY . .
RUN npm ci

COPY app .
RUN mkdir dist
