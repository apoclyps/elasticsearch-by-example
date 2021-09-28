import json
import logging
import sys

import ddtrace
import structlog
from ddtrace import tracer
from flask import request

LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARNING,
    "error": logging.ERROR,
}

log = structlog.get_logger()


def context(**kwargs):
    structlog.threadlocal.bind_threadlocal(**kwargs)
    if (span := tracer.current_root_span()) is not None:
        span.set_tags(kwargs)


def clear_context():
    structlog.threadlocal.clear_threadlocal()


def clear_celery_context(
    self, status, retval, task_id, args, kwargs, einfo  # NOQA: U100
):
    clear_context()


def log_inbound_request(response):
    if request.path == "/healthz" or "static" in request.path:
        return response

    log_attrs = {
        "method": request.method,
        "path": request.path,
        "query_string": request.query_string.decode("utf-8"),
        "remote_addr": request.remote_addr,
        "status": response.status_code,
        "user_agent": request.user_agent.to_header(),
        "response_body": response.get_data(as_text=True),
    }

    if request.method in ["PATCH", "POST", "PUT"]:
        if "/auth/login" in request.path:
            request_body = request.json or {}
            request_body["password"] = "<redacted>"
            log_attrs["request_body"] = json.dumps(request_body)
        else:
            log_attrs["request_body"] = request.get_data(as_text=True)

    log.info("received request", **log_attrs)
    return response


def get_renderer(format):
    if format == "json":
        return structlog.processors.JSONRenderer()
    else:
        return structlog.dev.ConsoleRenderer()


def tracer_injection(logger, log_method, event_dict):  # NOQA: U100
    # get correlation ids from current tracer context
    trace_id = None
    span_id = None

    if span := tracer.current_span():
        trace_id = span.trace_id
        span_id = span.span_id

    # add ids to structlog event dictionary
    event_dict["dd.trace_id"] = trace_id or 0
    event_dict["dd.span_id"] = span_id or 0

    # add the env, service, and version configured for the tracer
    event_dict["dd.env"] = ddtrace.config.env or ""
    event_dict["dd.service"] = ddtrace.config.service or ""
    event_dict["dd.version"] = ddtrace.config.version or ""

    return event_dict


def init_app(app):
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.disabled = True

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=LOG_LEVELS[app.config["LOG_LEVEL"]],
    )

    structlog.configure(
        processors=[
            structlog.threadlocal.merge_threadlocal,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            tracer_injection,
            get_renderer(app.config["LOGFMT"]),
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    app.before_request(clear_context)
    app.after_request(log_inbound_request)
