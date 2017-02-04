FROM yyolk/rpi-archlinuxarm:latest

RUN pacman -Sy python3 python-pip --noconfirm --noprogressbar &&\
  pip3 install --upgrade Flask google-api-python-client &&\
  rm -rf /var/cache/pacman/pkg/*

WORKDIR /app/

COPY expense_reporter.py /app/app.py
COPY client_secret.json /app/

CMD ["python3", "app.py"]
