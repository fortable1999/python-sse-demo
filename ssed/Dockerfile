FROM golang:1.10.0-alpine3.7

ARG HTTP_PROXY
ARG HTTPS_PROXY

RUN apk add --update --no-cache alpine-sdk bash ca-certificates \
      libressl \
      tar \
      git openssh openssl yajl-dev zlib-dev cyrus-sasl-dev openssl-dev build-base coreutils
WORKDIR /root
RUN git clone https://github.com/edenhill/librdkafka.git
WORKDIR /root/librdkafka
RUN /root/librdkafka/configure
RUN make
RUN make install
#For golang applications
RUN mkdir /lib64 && ln -s /lib/libc.musl-x86_64.so.1 /lib64/ld-linux-x86-64.so.2

ENV MYPROJECT "fortable1999/ssed"
WORKDIR /go/src/github.com/$MYPROJECT

RUN go get -d -v github.com/confluentinc/confluent-kafka-go/kafka

COPY . .
RUN GOOS=linux go get ./...
RUN GOOS=linux go install

# ENV PORT 4000
# EXPOSE ${PORT}
CMD ["ssed"]
