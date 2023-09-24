FROM python:3.10-alpine
LABEL authors="Red"
WORKDIR '/app'

COPY requirements.txt /tmp/requirements.txt

COPY redttg_mail_backend ./redttg_mail_backend
COPY scrape ./scrape
COPY templates ./templates
COPY manage.py .
COPY entrypoint.sh .

RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev gcc linux-headers

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

# consistent folders for data
RUN mkdir /app/covers
RUN mkdir /tmp/videos

# enable the entry file for execution
RUN chmod +x /app/entrypoint.sh

ENV DJANGO_SETTINGS_MODULE=ucha_hack_api.settings
ENV DEBUG=0

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]