import call_events.server as server
import logging


if __name__ == "__main__":
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    server.app.run(port=8080)
