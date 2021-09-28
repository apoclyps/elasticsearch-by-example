from typing import Tuple, Union

import flask

Response = Tuple[Union[flask.wrappers.Response, str], int]
