from app.module import bp, create, delete, get, update
from flask import request


@bp.route("/", methods=["POST"])
def create_route():
    return create.create(request)


@bp.route("/<moduleId>", methods=["DELETE"])
def delete_route(moduleId):
    return delete.delete(request, moduleId)


@bp.route("/<moduleId>", methods=["GET"])
def get_route(moduleId):
    return get.get(request, moduleId)


@bp.route("/<moduleId>", methods=["PUT"])
def update_route(moduleId):
    return update.update(request, moduleId)
