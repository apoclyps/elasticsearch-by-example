from marshmallow import EXCLUDE, Schema
from marshmallow_oneofschema import OneOfSchema


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class BaseOneOfSchema(OneOfSchema):
    class Meta:
        unknown = EXCLUDE
