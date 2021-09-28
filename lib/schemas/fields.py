import functools

from marshmallow import fields
from marshmallow_enum import EnumField

Boolean = functools.partial(fields.Boolean, allow_none=False, required=True)
Date = functools.partial(fields.Date, allow_none=False, required=True)
DateTime = functools.partial(fields.DateTime, allow_none=False, required=True)
Decimal = functools.partial(
    fields.Decimal, allow_none=False, required=True, places=2, as_string=True
)
Dict = functools.partial(fields.Dict, allow_none=False, required=True)
Enum = EnumField
Float = functools.partial(fields.Float, allow_none=False, required=True)
Function = functools.partial(fields.Function, allow_none=False, required=True)
Integer = functools.partial(fields.Integer, allow_none=False, required=True)
List = functools.partial(fields.List, allow_none=False, required=True)
Nested = functools.partial(fields.Nested, allow_none=False, required=True)
String = functools.partial(fields.String, allow_none=False, required=True)
UUID = functools.partial(fields.UUID, allow_none=False, required=True)
