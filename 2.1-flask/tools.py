from schema import SCHEMA_CLASS
from pydantic import ValidationError
from errors import HttpError


def validate(schema_cls: SCHEMA_CLASS, json_date: dict | list):
    try:
        return schema_cls(**json_date). dict(exclude_unset = True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)