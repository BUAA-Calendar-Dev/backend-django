import json
from itertools import chain

from django.db import models
from django.http import HttpRequest


def parse_request(request: HttpRequest) -> dict | None:
    """Parse request body and generate python dict

    Args:
        request (HttpRequest): all http request

    Returns:
        | request body is malformed = None
        | otherwise                 = python dict
    """
    try:
        return json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return None
