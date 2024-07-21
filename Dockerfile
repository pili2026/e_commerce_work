FROM python:3.12.2-slim

WORKDIR /app

COPY . /app

ENV PYTHONPATH=./src:$PYTHONPATH

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "./docker_entrypoint/web_api_server_entrypoint.sh" ]