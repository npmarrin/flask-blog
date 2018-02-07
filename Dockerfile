# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
FROM python:3.6.4-slim-stretch
COPY . /opt/flask/blog
WORKDIR /opt/flask/blog
ENV DEBIAN_FRONTEND=noninteractive

# https://askubuntu.com/questions/49196/how-do-i-create-a-self-signed-ssl-certificate
RUN /usr/bin/apt-get update \
&& /usr/bin/apt-get install ssl-cert \
&& /usr/sbin/make-ssl-cert generate-default-snakeoil
RUN /usr/local/bin/pip install -r requirements.txt
ENV PYTHONPATH=/opt/flask/blog
CMD ["/usr/local/bin/python", "-m", "flask_blog.app"]
