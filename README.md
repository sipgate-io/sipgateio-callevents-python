<img src="https://www.sipgatedesign.com/wp-content/uploads/wort-bildmarke_positiv_2x.jpg" alt="sipgate logo" title="sipgate" align="right" height="112" width="200"/>

# sipgate.io Python call events example
This example demonstrates how to receive and process webhooks from [sipgate.io](https://developer.sipgate.io/).

For further information regarding the push functionalities of sipgate.io please visit https://developer.sipgate.io/push-api/api-reference/

- [Prerequisites](#Prerequisites)
- [Enabling sipgate.io for your sipgate account](#Enabling-sipgateio-for-your-sipgate-account)
- [How sipgate.io webhooks work](#How-sipgateio-webhooks-work)
- [Configure webhooks for sipgate.io](#Configure-webhooks-for-sipgateio)
- [A word on security](#A-word-on-security)
- [Making your computer accessible from the internet](#Making-your-computer-accessible-from-the-internet)
- [Get the code example:](#Get-the-code-example)
- [Install dependencies:](#Install-dependencies)
- [Configuration](#Configuration)
- [Execution](#Execution)
- [How It Works](#How-It-Works)
- [Common Issues](#Common-Issues)
- [Related](#Related)
- [Contact Us](#Contact-Us)
- [License](#License)
- [External Libraries](#External-Libraries)


## Prerequisites
- python3
- pip3


## Enabling sipgate.io for your sipgate account
In order to use sipgate.io, you need to book the corresponding package in your sipgate account. The most basic package is the free **sipgate.io S** package.

If you use [sipgate basic](https://app.sipgatebasic.de/feature-store) or [simquadrat](https://app.simquadrat.de/feature-store) you can book packages in your product's feature store.
If you are a _sipgate team_ user logged in with an admin account you can find the option under **Account Administration**&nbsp;>&nbsp;**Plans & Packages**.


## How sipgate.io webhooks work

### What is a webhook?
A webhook is a POST request that sipgate.io makes to a predefined URL when a certain event occurs.
These requests contain information about the event that occurred in `application/x-www-form-urlencoded` format.

This is an example payload converted from `application/x-www-form-urlencoded` to JSON:
```json
{
  "event": "newCall",
  "direction": "in",
  "from": "492111234567",
  "to": "4915791234567",
  "callId":"12345678",
  "origCallId":"12345678",
  "user": [ "Alice" ],
  "xcid": "123abc456def789",
  "diversion": "1a2b3d4e5f"
}
```


### sipgate.io webhook events
sipgate.io offers webhooks for the following events:

- **newCall:** is triggered when a new incoming or outgoing call occurs 
- **onAnswer:** is triggered when a call is answered – either by a person or an automatic voicemail
- **onHangup:** is triggered when a call is hung up
- **dtmf:** is triggered when a user makes an entry of digits during a call

**Note:** Per default, sipgate.io only sends webhooks for **newCall** events.
To subscribe to other event types you can reply to the **newCall** event with an XML response.
This response includes the event types you would like to receive webhooks for as well as the respective URL they should be directed to.
You can find more information about the XML response here:
https://developer.sipgate.io/push-api/api-reference/#the-xml-response


## Configure webhooks for sipgate.io 
You can configure webhooks for sipgate.io as follows:

1. Navigate to [console.sipgate.com](https://console.sipgate.com/) and login with your sipgate account credentials.
2. Select the **Webhooks**&nbsp;>&nbsp;**URLs** tab in the left side menu
3. Click the gear icon of the **Incoming** or **Outgoing** entry
4. Fill in your webhook URL and click save. \
**Note:** your webhook URL has to be accessible from the internet. (See the section [Making your computer accessible from the internet](#making-your-computer-accessible-from-the-internet))\
**Example:** Assuming your server's address was `example.localhost.run`, the address you'd need to set in the webhook console would be `https://example.localhost.run/new-call`.
5. In the **sources** section you can select what phonelines and groups should trigger webhooks.

## A word on security
Although sipgate.io can work with both HTTP and HTTPS connections, it is strongly discouraged to use plain HTTP as the webhooks contain sensitive information.
The service `localhost.run` also supports HTTPS, so for development you will be fine using that.
For production, it is important to note that sipgate.io does not accept self-signed SSL certificates.
If you need a certificate for your server, you can easily get one at _Let´s Encrypt_.

## Making your computer accessible from the internet
There are many possibilities to obtain an externally accessible address for your computer.
In this example we use the service [localhost.run](localhost.run) which sets up a reverse ssh tunnel that forwards traffic from a public URL to your localhost.
The following command creates a subdomain at localhost.run and sets up a tunnel between the public port 80 on their server and your localhost:8080:

```bash
$ ssh -R 80:localhost:8080 ssh.localhost.run
```
If you run this example on a server which can already be reached from the internet, you do not need the forwarding.
In that case, the webhook URL needs to be adjusted accordingly.


## Get the code example:
Clone Repository with HTTPS
```bash
git clone https://github.com/sipgate-io/sipgateio-callevents-python.git
```

Clone Repository with SSH
```bash
git clone git@github.com/sipgate-io/sipgateio-callevents-python.git
```

Navigate to the project's root directory.


## Install dependencies:
Please run the following command:
```bash
$ pip3 install -r requirements.txt
```

## Configuration
Create the `.env` by copying the [`.env.example`](.env.example) and set the values according to the comment above the variables.

The `WEBHOOK_URL` is the URL under which your server is accessible from the internet (i.e. the URL you set up in the webhooks console minus the "`/new-call`" portion) (See [Configure webhooks for sipgate.io](#configure-webhooks-for-sipgateio)).

In the `server.py` the `ON_ANSWER_URL` and `ON_HANGUP_URL` is set to the `WEBHOOK_URL` followed by a suffix depending on the event type.
```python
ON_ANSWER_URL = WEBHOOK_URL + "/on-answer"
ON_HANGUP_URL = WEBHOOK_URL + "/on-hangup"
```

## Execution
Run the application:
```bash
python -m call_events 
```

## How It Works

In the `__main__.py`, which is a starting point of the application, we import the `server` module from our file `server.py` on the same directory.
The library _logging_ is imported to reduce the log report of the _Flask_ framework to only print errors. The `server` module contains a _Flask_ application called `app`, which is started by calling its `run()` method with the desired port.  

```python
import call_events.server as server
import logging
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    server.app.run(port=int(os.environ.get("WEBHOOK_PORT")))
```
The application's behavior is defined in the `server.py` script.

First, the necessary libraries are imported, _Flask_ for starting the server and _ElementTree_ for creating the xml responses:
```python
import flask
import xml.etree.ElementTree as ET
```

Following the HTTP server gets created using the _Flask_ framework:
```python
app = flask.Flask(__name__)
```

Afterwards, the routes are specified which handles the incoming POST requests.

With the function `handle_new_call()` a xml response is returned containing urls for the following events. 
```python
@app.route("/new-call", methods=["POST"])
def handle_new_call():
    request = flask.request
    request_data = request.form.to_dict()

    caller = request_data.get("from", "[unknown]")
    callee_number = request_data.get("to", "[unknown]")

    print("New call from {} to {} is ringing...".format(caller, callee_number))

    xml_response = build_xml_response()
    return xml_response, 200, {"Content-Type": "application/xml"}
```

Within the function `handle_new_call()`, the caller and callee_number are read from the request data and are printed.
```python
caller = request_data.get("from", "[unknown]")
callee_number = request_data.get("to", "[unknown]")

print("New call from {} to {} is ringing...".format(caller, callee_number))
```

Afterwards the xml response get created. Therefore the function `build_xml_response()` is called. 
It returns a xml response string and the corresponding HTTP status code `204` indicating that there is no content:
```python
xml_response = build_xml_response()
```

After that the attributes `onAnswer` and `onHangup` are added to the `Response` element containing the url earlier defined for the following events.
Within the `build_xml_response()` function, an instance of an ElementTree is created. The created element is called `Response`. 

```python
def build_xml_response():
    response = ET.Element("Response")
    response.set("onAnswer", ON_ANSWER_URL)
    response.set("onHangup", ON_HANGUP_URL)
    xml_response = ET.tostring(response)
    return xml_response
```

The function ``handle_on_answer()`` is similar to the previous one ``handle_new_call()``, except there is no xml response.

```python
@app.route("/on-answer", methods=["POST"])
def handle_on_answer():
    request = flask.request
    request_data = request.form.to_dict()

    caller = request_data.get("from", "[unknown]")
    callee_name = request_data.get("user", "[unknown]")

    print("{} answered call from {}".format(callee_name, caller))

    return "This response will be discarded", 200
```

For the `Hangup event` a method ``handle_on_hangup()`` is created, to notify that the call has been hung up.

```python
@app.route("/on-hangup", methods=["POST"])
def handle_on_hangup():
    print("The call has been hung up")

    return "This response will be discarded", 200
```

## Common Issues

### web app displays "Feature sipgate.io not booked."
Possible reasons are:
- the sipgate.io feature is not booked for your account

See the section [Enabling sipgate.io for your sipgate account](#enabling-sipgateio-for-your-sipgate-account) for instruction on how to book sipgate.io


### "OSError: [Errno 98] Address already in use"
Possible reasons are:
- another instance of the application is already running
- the specified port is in use by another application


### "PermissionError: [Errno 13] Permission denied"
Possible reasons are:
- you do not have permission to bind to the specified port.
  This usually occurs if you try to use port 80, 443 or another well-known port which can only be bound with superuser privileges


### Call happened but no webhook was received 
Possible reasons are:
- the configured webhook URL is incorrect
- the SSH tunnel connection was closed in the background
- webhooks are not enabled for the phoneline that received the call


## Related
- [Flask](http://flask.pocoo.org/)


## Contact Us
Please let us know how we can improve this example.
If you have a specific feature request or found a bug, please use **Issues** or fork this repository and send a **pull request** with your improvements.


## License
This project is licensed under **The Unlicense** (see [LICENSE file](./LICENSE)).


## External Libraries
This code uses the following external libraries

- _Flask_:
  - Licensed under the [BSD License](http://flask.pocoo.org/docs/1.0/license/)
  - Website: http://flask.pocoo.org//


---

[sipgate.io](https://www.sipgate.io) | [@sipgateio](https://twitter.com/sipgateio) | [API-doc](https://api.sipgate.com/v2/doc)
