# How to use
```
docker run --rm  -p 5044:5044 --net=host --name=logstash -it -d -v ~/pipeline/:/usr/share/logstash/pipeline/ docker.elastic.co/logstash/logstash:6.3.1
```
