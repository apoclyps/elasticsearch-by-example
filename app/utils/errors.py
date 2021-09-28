class MalformedDatetimeError(Exception):
    """Unable to parse the datetime provided"""

    pass


class RequiredURLParameterError(Exception):
    """Unable to process request as a required URL parameter is missing"""

    pass


class ExceedMaximumPaginationError(Exception):
    """Unable to process request as a pagination exceed the maximum results per page."""

    pass


class InvalidUUIDError(Exception):
    """Unable to parse UUID"""

    pass


class NotFoundError(Exception):
    """Unable to find the target resource"""

    pass


class UnprocessableEntityError(Exception):
    """Unable to save a resource as indicates the server understands the content type of
    the request entity, and the syntax of the request entity is correct, but it was
    unable to process the contained instructions
    """

    pass
