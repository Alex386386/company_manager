FROM python:3.12-slim

WORKDIR /

COPY ./functions_servise/requirements.txt /

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

COPY ./functions_servise /

COPY ./common_models /common_models

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]