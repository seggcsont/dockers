import datetime

import flask
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client.service_account import ServiceAccountCredentials

SPREADSHEETID = "1ZIU-a7A-YEfz0oQtMDjhjkFIpqiAqqEtBrNza8RXmqs"

oauth_scopes = ['https://www.googleapis.com/auth/spreadsheets']

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

    @staticmethod
    def translate_to_letter(x):
        letters = [chr(i) for i in range(ord('A'), ord('Z'))]
        return x if isinstance(x, str) else letters[x]


def find_first_empty_row():
    sheet = get_sheet_service().spreadsheets().get(spreadsheetId=SPREADSHEETID,
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


def get_sheet_service():
    return discovery.build('sheets', 'v4', http=http_auth)


def update_sheet(title, amount, row):
    update_sheet_body = dict()
    update_sheet_body['values'] = [[formatted_date(), title + " (Bot)", amount]]
    _range = Range(Cell(0, row), Cell(2, row))
    sheet_resp = get_sheet_service().spreadsheets().values().update(
        spreadsheetId=SPREADSHEETID,
        range=_range.to_range_str(),
        valueInputOption='RAW',
        body=update_sheet_body).execute()
    sheet_resp['message'] = "{0} stored as '{1}' in the {2} line.".format(amount, title, row + 1)
    return sheet_resp


@app.route("/ping")
def ping():
    return "pong"


@app.route('/', methods=['GET'])
def index():
    title = flask.request.args.get("title")
    amount = flask.request.args.get("amount")

    if not title or not amount:
        flask.abort(400)

    first_empty_row = find_first_empty_row()

    sheet_resp = update_sheet(title, amount, first_empty_row)

    return flask.Response(sheet_resp['message'], mimetype="text/plain")


if __name__ == '__main__':
    import uuid

    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run("0.0.0.0")
