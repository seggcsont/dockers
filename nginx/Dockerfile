FROM armhfbuild/nginx

COPY ssl/* /etc/nginx/certs/

RUN chmod 400 /etc/nginx/certs/*

COPY nginx.conf /etc/nginx/conf.d/default.conf
