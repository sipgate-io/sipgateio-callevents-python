import flask
import xml.etree.ElementTree as ET

BASE_URL = "[YOUR_SERVERS_ADDRESS]'

ON_ANSWER_URL = BASE_URL + "/on-answer"
ON_HANGUP_URL = BASE_URL + "/on-hangup"

app = flask.Flask(__name__)


@app.route("/new-call", methods=["POST"])
def handle_new_call():
    request = flask.request
    request_data = request.form.to_dict()

    caller = request_data.get("from", "[unknown]")
    callee_number = request_data.get("to", "[unknown]")

    print("New call from {} to {} is ringing...".format(caller, callee_number))

    xml_response = build_xml_response()
    return xml_response, 200, {"Content-Type": "application/xml"}


@app.route("/on-answer", methods=["POST"])
def handle_on_answer():
    request = flask.request
    request_data = request.form.to_dict()

    caller = request_data.get("from", "[unknown]")
    callee_number = request_data.get("to", "[unknown]")

    print("{} answered call from {}".format(callee_number, caller))

    return "This response will be discarded", 200


@app.route("/on-hangup", methods=["POST"])
def handle_on_hangup():
    print("The call has been hung up")

    return "This response will be discarded", 200


def build_xml_response():
    response = ET.Element("Response")
    response.set("onAnswer", ON_ANSWER_URL)
    response.set("onHangup", ON_HANGUP_URL)
    xml_response = ET.tostring(response)
    return xml_response
