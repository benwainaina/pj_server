FROM python:3.9-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update \
    && apk add build-base \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev libjpeg libwebp-dev \
    && apk add libffi-dev && apk add curl
ENV APP_HOME=/app
WORKDIR $APP_HOME
COPY . $APP_HOME
RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt
RUN mkdir -p $APP_HOME/static
RUN mkdir -p $APP_HOME/media
RUN mkdir -p $APP_HOME/logs