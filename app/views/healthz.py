from flask import Blueprint, jsonify

from lib import instrumentation

blueprint = Blueprint("healthz", __name__)
blueprint_public = Blueprint("healthz_public", __name__, url_prefix="/public")


@blueprint.route("/healthz", methods=["GET"])
@blueprint_public.route("", methods=["GET"])
def get_healthz():
    instrumentation.suppress_transaction()
    return jsonify({"success": True}), 200
