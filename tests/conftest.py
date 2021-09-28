import json
import os.path
from typing import Dict, Tuple

import pytest
import frontmatter
from elasticsearch import Elasticsearch

from app import create_app


@pytest.fixture
def load_json():
    def _load_json(fixture_path):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), fixture_path)
        with open(path) as f:
            data = f.read()
        return json.loads(data)

    return _load_json


@pytest.fixture
def load_event_fixture():
    def _load_event_fixture(sample_file):
        return json.loads(_load_sample(f"{sample_file}").content)

    return _load_event_fixture


@pytest.fixture
def load_event_sample():
    def _load_event_sample(sample_file: str) -> Dict:
        """
        Given a filename, load the sample event
        :param sample_file: Filename to load from /docs/events/
        :return: Dict of event
        """
        event = _load_sample(f"docs/events/{sample_file}")
        return {**event.metadata, "body": json.loads(event.content)}

    return _load_event_sample


def _load_sample(fixture_path):
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), os.path.pardir, fixture_path
    )
    return frontmatter.load(path)


@pytest.fixture
def load_api_sample():
    def _load_api_sample(sample_file: str) -> Tuple[Dict, Dict]:
        """
        Given a filename, load the sample request and matching response
        :param sample_file: Filename to load from /docs/requests/
        :return: Two-tuple of request, and expected response
        """
        req = _load_sample(f"docs/requests/{sample_file}")
        res = _load_sample(req.metadata["response"])
        return {**req.metadata, "body": json.loads(req.content)}, {
            **res.metadata,
            "body": json.loads(res.content),
        }

    return _load_api_sample


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture
def client(app):
    app.testing = True

    return app.test_client()


@pytest.fixture(scope="session")
def elasticsearch_client():
    return Elasticsearch(hosts=["test-elasticsearch"])
