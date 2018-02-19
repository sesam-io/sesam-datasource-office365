import requests
from flask import Flask, Response
import os
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.runtime.client_request import ClientRequest
from office365.runtime.utilities.request_options import RequestOptions
import logging

app = Flask(__name__)
url = os.environ.get("baseurl")
username = os.environ.get("username")
password = os.environ.get("password")


@app.route("/<path:path>", methods=["GET"])
def get(path):
    if url is not None or username is not None or password is not None:
        try:
            ctx_auth = AuthenticationContext(url)
            if ctx_auth.acquire_token_for_user(username, password):
                ClientRequest(ctx_auth)
                request_url = "{0}{1}".format(url, path)
                log.info("Getting '{0}' from '{1}'".format(path, url))
                options = RequestOptions("{0}".format(request_url))
                options.set_header('Accept', 'application/json')
                options.set_header('Content-Type', 'application/text')
                ctx_auth.authenticate_request(options)
                data = requests.get(url=options.url, headers=options.headers, auth=options.auth)
            return Response(data.content, mimetype="application/text")
        except BaseException as e:
            log.exception("Failed to get resource '{0}': {1}".format(request_url, e))
            raise e
    else:
        raise ValueError("Missing one or more required environment variables (baseurl, username, password)")


def init_logging():
    # Set up logging
    format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logger = logging.getLogger('sesam-office365-csvfileshare')

    # Log to stdout
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(logging.Formatter(format_string))
    logger.addHandler(stdout_handler)

    loglevel = os.environ.get("loglevel", "INFO")
    if "INFO" == loglevel.upper():
        logger.setLevel(logging.INFO)
    elif "DEBUG" == loglevel.upper():
        logger.setLevel(logging.DEBUG)
    elif "WARN" == loglevel.upper():
        logger.setLevel(logging.WARN)
    elif "ERROR" == loglevel.upper():
        logger.setLevel(logging.ERROR)
    else:
        logger.setlevel(logging.INFO)
        logger.info("Unsupported loglevel defined. Using default level: INFO.")
    return logger


if __name__ == '__main__':
    log = init_logging()

    app.run(debug=True, host='0.0.0.0', threaded=True, port=os.environ.get('port',5000))