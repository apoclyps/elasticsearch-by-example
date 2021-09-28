#!/usr/local/bin/python

from typing import Dict

import click
import frontmatter
import yaml
from apispec import APISpec
from apispec.utils import deepupdate
from apispec_oneofschema import MarshmallowPlugin
from marshmallow_enum import EnumField

from lib.schemas import BaseSchema

EXAMPLES: Dict[str, str] = {}

SCHEMAS: Dict[str, BaseSchema] = {}


def enum_to_properties(self, field, **kwargs):  # NOQA: U100
    if isinstance(field, EnumField):
        return {"type": "string", "enum": [m.name for m in field.enum]}
    return {}


def load(path):
    return frontmatter.load(path).content


def build(version="3.0.3", examples=EXAMPLES, schemas=SCHEMAS):
    marshmallow_plugin = MarshmallowPlugin()

    builder = APISpec(
        title="Reporting Service",
        version="",
        openapi_version=version,
        plugins=[marshmallow_plugin],
    )

    marshmallow_plugin.converter.add_attribute_function(enum_to_properties)

    for name, example in examples.items():
        builder.components.example(name, {"value": load(example)})

    for name, schema in schemas.items():
        builder.components.schema(name, schema=schema)

    return builder.to_dict()


def apply_template(spec, template_path="./docs/openapi.template.yaml"):
    with open(template_path) as file:
        template = yaml.load(file, Loader=yaml.SafeLoader)

    return deepupdate(spec, template)


def document():
    spec = build()
    spec = apply_template(spec)
    return yaml.dump(spec, sort_keys=False)


@click.command()
@click.option("--path")
def cli(path):
    with open(path, "w") as file:
        file.write(document())


if __name__ == "__main__":
    cli()
