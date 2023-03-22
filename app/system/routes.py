from app.system import bp, start, stop, restart, status
from flask import request


@bp.route("/start", methods=["GET"])
def start_route():
    return start.start(request)


@bp.route("/stop", methods=["GET"])
def stop_route():
    return stop.stop(request)


@bp.route("/restart", methods=["GET"])
def restart_route():
    return restart.restart(request)


@bp.route("/status", methods=["GET"])
def status_route():
    return status.status(request)
