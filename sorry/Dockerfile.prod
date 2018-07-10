FROM httpd:latest
COPY ./filebeat-6.3.0-amd64.deb /root/filebeat-6.3.0-amd64.deb
COPY ./httpd.conf /usr/local/apache2/conf/.
RUN dpkg -i /root/filebeat-6.3.0-amd64.deb
COPY ./filebeat.yml /etc/filebeat/filebeat.yml
RUN chmod go-w /etc/filebeat/filebeat.yml
CMD httpd; filebeat -e -c /etc/filebeat/filebeat.yml
