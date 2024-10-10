FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry==1.8.3

COPY . /app

RUN poetry install

CMD ["poetry", "run", "python", "src/main.py"]