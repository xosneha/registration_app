FROM python:3.11

WORKDIR /fastapi

RUN pip install "poetry==1.5.1" && \
    poetry config virtualenvs.create false

ADD pyproject.toml poetry.lock /fastapi/
ADD /registration_app /fastapi/registration_app/

RUN poetry install --no-dev

CMD ["uvicorn", "registration_app.api.main:app", "--host", "0.0.0.0", "--port", "5001"]



