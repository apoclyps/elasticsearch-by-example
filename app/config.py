from decouple import config

DATADOG_TRACE_ENABLED = config("DATADOG_TRACE_ENABLED", cast=bool)
DISABLE_AUTH = config("DISABLE_AUTH", cast=bool)
FLASK_ENV = config("FLASK_ENV")
HTTP_CLIENT_TIMEOUT = config("HTTP_CLIENT_TIMEOUT", cast=int, default=5)
LOG_LEVEL = config("LOG_LEVEL")
LOGFMT = config("LOGFMT")

# Elasticsearch Configuration
ELASTICSEARCH_HOST = config("ELASTICSEARCH_HOST")
ELASTICSEARCH_MAX_CONNECTIONS = config(
    "ELASTICSEARCH_MAX_CONNECTIONS", cast=int, default=10
)
ELASTICSEARCH_MAX_RETRIES = config("ELASTICSEARCH_MAX_RETRIES", cast=int, default=2)
ELASTICSEARCH_RETRY_ON_TIMEOUT = config(
    "ELASTICSEARCH_RETRY_ON_TIMEOUT", cast=bool, default=True
)
ELASTICSEARCH_TIMEOUT = config("ELASTICSEARCH_TIMEOUT", cast=int, default=5)
EVENT_INDEX_NAME = config("EVENT_INDEX_NAME", default="event-index")


if DISABLE_AUTH and FLASK_ENV != "development":
    raise Exception("Authentication can only be disabled for local development")
