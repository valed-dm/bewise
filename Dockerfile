FROM python:3.12-bookworm

WORKDIR /code

COPY ./requirements.txt /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 8000