FROM yyolk/rpi-archlinuxarm:latest

RUN groupadd --gid ${GROUP_ID-1000} transmission && useradd --gid transmission --create-home --uid ${USER_ID-1000} transmission

RUN pacman -Sy transmission-cli --noconfirm --noprogressbar \
  && rm -rf /var/cache/pacman/pkg/*

RUN mkdir -p /app/torrents && \
  chown -R transmission:transmission /app

USER transmission

ENV TRANSMISSION_USER "transmission"
ENV TRANSMISSION_PASSWORD "transmission"

CMD transmission-daemon --no-watch-dir --no-incomplete-dir --foreground --auth --username $TRANSMISSION_USER --password $TRANSMISSION_PASSWORD --allowed "*.*.*.*" --config-dir /app/ --download-dir /app/torrents
