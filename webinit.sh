#!/bin/bash
# https://google.github.io/styleguide/shell.xml

/usr/local/bin/flask db upgrade

if [[ "$1" == "true" ]]; then
  /usr/local/bin/flask run -h 0.0.0.0 --with-threads
else
  /usr/local/bin/gunicorn \
    -w 10 -b 0.0.0.0:5000 \
    --certfile /etc/ssl/certs/ssl-cert-snakeoil.pem \
    --keyfile /etc/ssl/private/ssl-cert-snakeoil.key \
    blog:app
fi