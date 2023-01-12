FROM nginx:1.21-alpine

COPY /static /var/www/static

RUN rm /etc/nginx/conf.d/default.conf
COPY *.conf /etc/nginx/conf.d/