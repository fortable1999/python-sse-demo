FROM python:3.6-stretch

ARG HTTP_PROXY
ARG HTTPS_PROXY

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python3", "app.py" ]
