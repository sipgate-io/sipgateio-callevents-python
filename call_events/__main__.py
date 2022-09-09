import call_events.server as server
import logging
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    server.app.run(port=int(os.environ.get("WEBHOOK_PORT")))
