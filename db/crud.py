"""SQLAlchemy ORM interacts with PostgreSQL"""

import os
from typing import Type

from dotenv import load_dotenv
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, scoped_session

from db.quiz import Quiz
from ext_api.jservice import get_questions

load_dotenv()

DB_URL = os.environ.get("PG_CONN_STR")
DB_ECHO = False

engine = create_engine(url=DB_URL, echo=DB_ECHO)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


def create_question(session: scoped_session, question: str, answer: str) -> None:
    """Creates new question record in db"""

    q: Quiz = Quiz(question=question, answer=answer)
    session.add(q)
    session.commit()


def get_all_questions(session: scoped_session) -> list[Type[Quiz]]:
    """Queries for all questions records from db"""

    questions = session.query(Quiz).all()
    return questions


def question_exists(session: scoped_session, question: str) -> bool:
    """Checks if the same record exists in db"""

    exists: bool = session.query(
        session.query(Quiz).filter_by(question=question).exists()
    ).scalar()

    return exists


def delete_question(session: scoped_session, question: Type[Quiz]) -> None:
    """Removes question record from db"""

    session.delete(question)
    session.commit()


def find_last_question(session: scoped_session) -> dict:
    """Searches for the last db record before update"""

    last_record: Type[Quiz] | None = session.query(Quiz).order_by(desc('id')).first()

    try:
        last_question = {
            "id": last_record.id,
            "question": last_record.question,
            "answer": last_record.answer,
            "created_at": last_record.created_at.strftime("%m/%d/%Y, %H:%M:%S")
        }
    except AttributeError:
        last_question = {}

    return last_question


def add_new_questions_to_db(questions: list[dict], recursive: bool = False) -> dict:
    """Returns last db record value and performs update"""

    last_question = {}
    session = Session()

    for i, q in enumerate(questions):
        answer: str = q["answer"]
        question: str = q["question"]
        # the last question is requested only once for a cycle
        if not recursive and i == 0:
            last_question = find_last_question(session=session)
            # print("search for last question done once for a cycle")

        if question_exists(session=session, question=question):
            # print("duplicated question encountered")
            session.close()
            # new question search starts to avoid duplication
            substitute_question = get_questions(1)
            # recursive function call till unique question will be obtained and stored
            add_new_questions_to_db(questions=substitute_question, recursive=True)
        else:
            create_question(session=session, question=question, answer=answer)

    session.close()

    return last_question


def main():
    """Main was used once only for db operations testing"""

    session: scoped_session = Session()

    questions = get_all_questions(session)
    for q in questions:
        delete_question(session, q)

    create_question(session, "How are you?", "Thanks, fine")
    create_question(session, "Are you ready?", "Yes, I am")

    questions = get_all_questions(session)
    for q in questions:
        print(q.question, q.answer)
        print(question_exists(session=session, question=q.question))
        print(question_exists(session=session, question="Test question"))

    session.close()


if __name__ == '__main__':
    main()
