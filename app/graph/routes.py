from flask import request

from app.graph import bp, logs, get, update


@bp.route("/logs/<name>", methods=["POST"])
def create_route(name):
    return logs.logs(request, name)


@bp.route("/", methods=["GET"])
def get_route():
    return get.get(request)


@bp.route("/", methods=["PUT"])
def update_route():
    return update.update(request)
