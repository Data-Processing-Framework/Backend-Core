from flask import request

from app.graph import bp, create, get, update


@bp.route("", methods=["POST"])
def create_route():
    return create.create(request)


@bp.route("", methods=["GET"])
def get_route():
    return get.get(request)


@bp.route("", methods=["PUT"])
def update_route():
    return update.update(request)
