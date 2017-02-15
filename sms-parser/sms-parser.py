import json
import re

from flask import Flask, Response, request
from pymongo import MongoClient, ReturnDocument

sms_pattern = re.compile(".*POS tranzakci. ([\d ]+).*Hely: (.+)")
app = Flask(__name__)
mongoc = MongoClient(host="mongodb")
db = mongoc.home_bot


def parse_sms(content):
    resp = dict()
    resp['content'] = content
    match = re.match(sms_pattern, content)
    if match:
        resp['amount'] = match.group(1).replace(' ', '')
        resp['location'] = match.group(2)
    else:
        print("SMS does not match: '%s'" % content)
    return resp


@app.route("/sms", methods=["POST"])
def parse():
    assert request.form['content']
    resp = parse_sms(request.form['content'])
    return Response(json.dumps(resp), mimetype="text/plain")


@app.route("/alias", methods=["POST"])
def add_alias():
    assert request.form['location']
    assert request.form['alias']
    updated_doc = db.aliases.find_one_and_update(
        {'location': request.form['location']},
        {"$push": {
            "aliases": request.form['alias']
        }},
        upsert=True,
        return_document=ReturnDocument.AFTER,
        projection={'_id': False}
    )
    return json.dumps(updated_doc), 201


if __name__ == '__main__':
    import uuid

    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run("0.0.0.0")
