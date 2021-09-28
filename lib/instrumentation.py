from ddtrace import tracer
from ddtrace.constants import MANUAL_DROP_KEY


def record_exception() -> None:
    if (span := tracer.current_root_span()) is not None:
        span.set_traceback()


def suppress_transaction() -> None:
    if (span := tracer.current_root_span()) is not None:
        span.set_tag(MANUAL_DROP_KEY)
