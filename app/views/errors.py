import traceback

from flask import Blueprint, jsonify
from marshmallow.exceptions import ValidationError
from requests import HTTPError
from werkzeug.exceptions import HTTPException

from app import config
from app.utils.errors import (
    ExceedMaximumPaginationError,
    InvalidUUIDError,
    MalformedDatetimeError,
    NotFoundError,
    RequiredURLParameterError,
    UnprocessableEntityError,
)
from lib import instrumentation

blueprint = Blueprint("errors", __name__)


STATUS_CODES = {
    RequiredURLParameterError: 400,
    ExceedMaximumPaginationError: 400,
    StopIteration: 404,
    NotFoundError: 404,
    UnprocessableEntityError: 422,
    InvalidUUIDError: 422,
    MalformedDatetimeError: 422,
    ValidationError: 422,
}


@blueprint.app_errorhandler(Exception)
def handle_error(e):
    instrumentation.record_exception()
    return jsonify(_build_payload(e)), _map_status(e)


def _build_payload(e):
    if config.FLASK_ENV in ("development", "test"):
        return {
            "class": type(e).__name__,
            "message": str(e),
            "code": _map_status(e),
            "traceback": [
                f"{tb.filename}:{tb.lineno}: {tb.name}"
                for tb in traceback.extract_tb(e.__traceback__)
            ],
        }

    return {"message": str(e), "code": _map_status(e)}


def _map_status(e):
    if isinstance(e, HTTPException):
        return e.get_response().status_code

    if isinstance(e, HTTPError):
        return e.response.status_code

    for error_type, status in STATUS_CODES.items():
        if isinstance(e, error_type):
            return status

    return 500
