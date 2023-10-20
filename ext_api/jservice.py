"""Requests data from jservice server"""

import requests


def get_questions(qty: int) -> list[dict]:
    """API jservice request"""

    req_string: str = f"https://jservice.io/api/random?count={qty}"

    try:
        response: requests.Response = requests.get(req_string, timeout=10)
        questions: list[dict] = response.json()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e) from e

    return questions
