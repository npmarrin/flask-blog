# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
FROM python:3.6.4-slim-stretch

ENV DEBIAN_FRONTEND=noninteractive
ENV FLASK_APP=blog
ENV FLASK_DEBUG=1
ENV PYTHONPATH=/opt/flask/blog

COPY . /opt/flask/blog
WORKDIR /opt/flask/blog

# https://askubuntu.com/questions/49196/how-do-i-create-a-self-signed-ssl-certificate
RUN /usr/bin/apt-get update \
&& /usr/bin/apt-get install ssl-cert \
&& /usr/sbin/make-ssl-cert generate-default-snakeoil

RUN /usr/local/bin/pip install -r requirements.txt

# Dev
# CMD ["/usr/local/bin/flask", "run", "-h", "0.0.0.0", "--with-threads"]
# Prod
CMD ["/usr/local/bin/gunicorn", "-w", "10", "-b", "0.0.0.0:5000", \
     "--certfile", "/etc/ssl/certs/ssl-cert-snakeoil.pem", \
     "--keyfile", "/etc/ssl/private/ssl-cert-snakeoil.key", "blog:app"]

