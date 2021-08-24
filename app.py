from flask import Flask
from flask import request, abort, jsonify, Response
from marshmallow import ValidationError
from schema import *

import logging
from pythonjsonlogger import jsonlogger

from werkzeug.exceptions import HTTPException, default_exceptions, _aborter

logger = logging.getLogger(__name__)
console_stream_handler = logging.StreamHandler()
console_stream_handler.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(name)s %(levelname)s %(message)s %(funcName)s"))
logger.addHandler(console_stream_handler)
logger.setLevel(logging.INFO)

def JsonApp(api):
    def error_handling(error):
        if isinstance(error, HTTPException):
            code = error.code
            result = {'error': error.description}
            logger.info({"message":"error"},extra=result)
        else:
            description = _aborter.mapping[500].description
            result = {'description': description,'error': str(error)}
            logger.error({'message':"error"}, extra=result)
        resp = jsonify(result)
        resp.status_code = code

        return resp

    for code in default_exceptions.keys():
        api.register_error_handler(code, error_handling)
    return api

app = JsonApp(Flask(__name__))


def _handle_validation_error(e: ValidationError) -> Response:
    resp = jsonify({'InvalidFields': e.normalized_messages()})
    resp.status_code = 400
    return resp

app.register_error_handler(ValidationError, _handle_validation_error)

@app.route("/")
def hello():
    return "Hello, World!"

@app.get("/<date>")
def date(date):
    get_user_schema = GetUserReponseSchema()
    payload = get_user_schema.load(request.get_json())
    return payload
