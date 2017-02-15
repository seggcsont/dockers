import json
import re

from flask import Flask, Response, request

sms_pattern = re.compile(".*POS tranzakci. ([\d ,]+).*Hely: (.+)")
app = Flask(__name__)


def parse_sms(content):
    resp = dict()
    resp['content'] = content
    match = re.match(sms_pattern, content)
    if match:
        resp['amount'] = match.group(1).replace(' ', '').replace(',', '')
        resp['location'] = match.group(2)
    else:
        print("SMS does not match: '%s'" % content)
    return resp


@app.route("/sms", methods=["POST"])
def parse():
    assert request.form['content']
    resp = parse_sms(request.form['content'])
    return Response(json.dumps(resp), mimetype="text/plain")


if __name__ == '__main__':
    import uuid

    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run("0.0.0.0")
