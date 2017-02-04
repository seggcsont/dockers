import datetime
import json

import flask
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client.service_account import ServiceAccountCredentials

oauth_scopes = ['https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", oauth_scopes)
http_auth = credentials.authorize(httplib2.Http())
app = flask.Flask(__name__)


class Range:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def to_range_str(self):
        return "%s%d:%s%d" % (self.start.x, self.start.y + 1, self.stop.x, self.stop.y + 1)


class Cell:
    def __init__(self, x, y):
        self.x = Cell.translate_to_letter(x)
        self.y = y

    def translate_to_letter(x):
        letters = [chr(i) for i in range(ord('A'), ord('Z'))]
        return x if isinstance(x, str) else letters[x]


def find_first_empty_row(sheet_service):
    sheet = sheet_service.spreadsheets().get(spreadsheetId="1ZIU-a7A-YEfz0oQtMDjhjkFIpqiAqqEtBrNza8RXmqs",
                                             ranges="A1:C142", includeGridData=True).execute()
    for _index, row in enumerate(sheet['sheets'][0]['data'][0]['rowData']):
        values = row['values']
        if len(values) == 3:
            for value in values:
                if value.get('formattedValue', "") != "":
                    break
            else:
                print("Empty row found: ", _index)
                return _index


def auth_required():
    return 'credentials' not in flask.session or client.OAuth2Credentials.from_json(
        flask.session['credentials']).access_token_expired


def formatted_date():
    return datetime.datetime.now().strftime("%d")


@app.route("/ping")
def ping():
    return "pong"


@app.route('/', methods=['GET'])
def index():
    title = flask.request.args.get("title")
    amount = flask.request.args.get("amount")

    if not title or not amount:
        flask.abort(400)
    sheet_service = discovery.build('sheets', 'v4', http=http_auth)

    first_empty_row = find_first_empty_row(sheet_service=sheet_service)

    update_sheet_body = dict()
    update_sheet_body['values'] = [[formatted_date(), title + " (Bot)", amount]]
    _range = Range(Cell(0, first_empty_row), Cell(2, first_empty_row))

    sheet_resp = sheet_service.spreadsheets().values().update(
        spreadsheetId="1ZIU-a7A-YEfz0oQtMDjhjkFIpqiAqqEtBrNza8RXmqs",
        range=_range.to_range_str(),
        valueInputOption='RAW',
        body=update_sheet_body).execute()

    sheet_resp['message'] = "{0} stored as '{1}' in the {2} line.".format(amount, title, first_empty_row + 1)

    return flask.Response(json.dumps(sheet_resp), mimetype="application/json")


if __name__ == '__main__':
    import uuid

    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run("0.0.0.0")
