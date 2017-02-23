FROM armhf/alpine

RUN apk update && \
    apk add --no-cache python3 && \
    pip3 install --upgrade Flask google-api-python-client

WORKDIR /app/

COPY expense_reporter.py /app/app.py

CMD ["python3", "app.py"]
