import json
from aiohttp.web import HTTPException

class Error(HTTPException):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description

        super(). __init__(
            text = json.dumps({"status": "error", "description": "description"}),
            content_typy = "application/json",
        )


class NotFound(Error):
        status_code = 404


class BadRequest(Error):
        status_code = 400


class Conflict(Error):
    status_code = 409


class Unauthorized(Error):
    status_code = 401


class Forbidden(Error):
    status_code = 403


class MethodNotAllowed(Error):
    status_code = 405


class UnexpectedError(Error):
    status_code = 500