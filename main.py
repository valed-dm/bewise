"""Fastapi main page"""

import json

from fastapi import FastAPI, Response

from db.crud import add_new_questions_to_db
from ext_api.jservice import get_questions
from schemas.qnum_post import Qnum

app = FastAPI()


@app.get('/')
def read_root() -> Response:
    """Handles root get request"""

    return Response(
        content='Quiz needs a POST request: {"qnum": int}',
        media_type='application/json'
    )


@app.post('/')
def read_post(data: Qnum) -> Response:
    """Reads root post request"""

    num: int = data.qnum
    questions: list[dict] = get_questions(num)
    previous_question: dict = add_new_questions_to_db(questions)

    return Response(
        content=json.dumps(previous_question),
        media_type='application/json'
    )
