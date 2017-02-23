FROM armhf/alpine

RUN addgroup -g ${GROUP_ID-1000} transmission && adduser -D -G transmission -u ${USER_ID-1000} transmission

RUN apk update &&\
    apk add --no-cache transmission-daemon &&\
    mkdir -p /app/torrents &&\
    chown -R transmission:transmission /app

USER transmission

ENV TRANSMISSION_USER "transmission"
ENV TRANSMISSION_PASSWORD "transmission"

CMD transmission-daemon --no-watch-dir --no-incomplete-dir --foreground --auth --username $TRANSMISSION_USER --password $TRANSMISSION_PASSWORD --allowed "*.*.*.*" --config-dir /app/ --download-dir /app/torrents
