FROM yyolk/rpi-archlinuxarm:latest

RUN pacman -Sy python3 python-pip --noconfirm --noprogressbar &&\
  pip3 install --upgrade Flask &&\
  rm -rf /var/cache/pacman/pkg/*

WORKDIR /app/

COPY sms-parser.py /app/app.py

CMD ["python3", "app.py"]
