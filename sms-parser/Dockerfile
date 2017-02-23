FROM armhf/alpine

RUN apk update &&\
    apk --no-cache add python3 &&\
    pip3 install --upgrade Flask pymongo

WORKDIR /app/

COPY sms-parser.py /app/app.py

CMD ["python3", "app.py"]
