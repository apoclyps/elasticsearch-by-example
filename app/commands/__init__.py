import click
import structlog

from app.commands.elasticsearch.indexes import elasticsearch_indexes

logger = structlog.get_logger()


@click.group()
def cli():
    pass


cli.add_command(elasticsearch_indexes)


if __name__ == "__main__":
    cli()
