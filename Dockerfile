FROM python:3.7.0

#ENV PIP_NO_CACHE_DIR=True
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=hashchat.settings

RUN pip3 install --upgrade pip
# Install system deps
RUN pip install "poetry==1.1.4"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Install with poetry
# pip install would probably work, too, but we'd have to make sure it's a recent enough pip
# Don't bother creating a virtual env -- significant performance increase
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

# Copy to workdir
COPY . /code


ARG GIT_HASH
ENV GIT_HASH=${GIT_HASH:-dev}
ENTRYPOINT [ "./docker-entrypoint.sh" ]