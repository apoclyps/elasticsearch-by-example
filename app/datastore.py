import structlog
from elasticsearch import Elasticsearch
from elasticsearch.connection import Urllib3HttpConnection

from app import config

logger = structlog.get_logger()


class LoggingConnection(Urllib3HttpConnection):
    """Override the default connection class to provide structured logging"""

    def log_request_success(
        self,
        method,
        full_url,
        path,
        body,  # NOQA: U100
        status_code,
        response,  # NOQA: U100
        duration,
    ):
        """Log a successful API call."""
        logger.debug(
            "Elasticsearch request success",
            http_method=method,
            full_url=full_url,
            path=path,
            duration=duration,
            status_code=status_code,
        )

    def log_request_fail(
        self,
        method,
        full_url,
        body,
        duration,
        status_code=None,
        response=None,
        exception=None,
    ):
        """Log an unsuccessful Elasticsearch API call."""
        # do not log 404s on HEAD requests
        if method == "HEAD" and status_code == 404:
            return

        logger.error(
            "Elasticsearch request failure",
            http_method=method,
            full_url=full_url,
            body=body,
            duration=duration,
            status_code=status_code,
            response=response,
            exc_info=exception is not None,
        )


elastic_search = Elasticsearch(
    connection_class=LoggingConnection,
    hosts=config.ELASTICSEARCH_HOST,
    maxsize=config.ELASTICSEARCH_MAX_CONNECTIONS,
    max_retries=config.ELASTICSEARCH_MAX_RETRIES,
    retry_on_timeout=config.ELASTICSEARCH_RETRY_ON_TIMEOUT,
    timeout=config.ELASTICSEARCH_TIMEOUT,
)
