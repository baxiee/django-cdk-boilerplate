FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /var/code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY local/docker/entrypoint.sh /scripts/
RUN chmod +x /scripts/entrypoint.sh

RUN ls && sleep 5
ENTRYPOINT ["sh", "/scripts/entrypoint.sh"]

EXPOSE 8000
