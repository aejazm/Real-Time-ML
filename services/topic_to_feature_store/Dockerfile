FROM python:3.12-slim

WORKDIR /app

# Install build-essential which includes gcc and other build tools
RUN apt-get update && apt-get install -y build-essential

RUN pip install poetry==1.8.3

COPY . /app

RUN poetry install

CMD ["poetry", "run", "python", "src/main.py"]