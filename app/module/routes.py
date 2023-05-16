from flask import request

from app.module import bp, create, delete, get, update


@bp.route("", methods=["POST"])
def create_route():
    return create.create(request)


@bp.route("/<name>", methods=["DELETE"])
def delete_route(name):
    return delete.delete(request, name)


@bp.route("/<name>", methods=["GET"])
def get_route(name):
    return get.get(request, name)


@bp.route("", methods=["GET"])
def get_route_all():
    return get.get(request, "")


@bp.route("/<name>", methods=["PUT"])
def update_route(name):
    return update.update(request, name)
