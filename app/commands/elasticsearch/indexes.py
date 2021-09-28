import click
import structlog

from app import config
from app.datastore import elastic_search
from lib.tools.elasticsearch import create_index, delete_index

logger = structlog.get_logger()


@click.group()
def elasticsearch_indexes():
    pass


@elasticsearch_indexes.command()
def create_indexes():
    from app import create_app

    app = create_app()

    with app.app_context():
        create_index(
            client=elastic_search,
            index_name=config.EVENT_INDEX_NAME,
            doc_type="event",
            logger=logger,
        )


@elasticsearch_indexes.command()
def delete_indexes():
    from app import create_app

    app = create_app()

    with app.app_context():
        delete_index(
            client=elastic_search, index_name=config.EVENT_INDEX_NAME, logger=logger
        )
