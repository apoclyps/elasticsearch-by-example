from flask import Blueprint

from scripts.docs import document

blueprint = Blueprint("docs", __name__)


@blueprint.route("/docs", methods=["GET"])
def get_openapi():
    content = document()
    headers = {"Content-Type": "text/yaml; charset=utf-8"}
    return content, 200, headers
