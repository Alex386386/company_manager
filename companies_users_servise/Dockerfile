FROM python:3.12-slim

WORKDIR /

COPY ./companies_users_servise/requirements.txt ./

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

COPY ./companies_users_servise /
COPY ./common_models /common_models
COPY ./alembic.ini /alembic.ini
COPY ./alembic /alembic

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]