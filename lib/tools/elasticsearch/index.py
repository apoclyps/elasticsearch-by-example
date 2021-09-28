import json

from elasticsearch import Elasticsearch
from structlog.stdlib import BoundLogger as StructLogger


def create_index(
    client: Elasticsearch, index_name: str, doc_type: str, logger: StructLogger
) -> None:
    """Create an index in Elasticsearch and apply the default mapping."""
    logger.info(f"attempting to create index: {index_name}")

    client.indices.create(index=index_name)
    logger.info(f"successfully created index: {index_name}")

    # apply mapping to the new index (removed in Elasticsearch 8.0)
    with open("mappings/{}.json".format(doc_type), "r") as f:
        mapping = json.loads(f.read())
    client.indices.put_mapping(
        index=index_name, doc_type=doc_type, body=mapping, include_type_name=True
    )
    logger.info(f"mapping applied for document type: {doc_type}")

    # add read/write aliases to the new index
    client.indices.put_alias(index=index_name, name=f"{index_name}-read")
    client.indices.put_alias(index=index_name, name=f"{index_name}-write")
    logger.info(f"aliases applied to the new index:: {doc_type}")


def delete_index(client: Elasticsearch, index_name: str, logger: StructLogger) -> None:
    """Delete an index from Elasticsearch."""
    logger.info(f"attempting to delete index: {index_name}")

    client.indices.delete(index=index_name, ignore=[404])
    logger.info(f"deleted index: {index_name}")
