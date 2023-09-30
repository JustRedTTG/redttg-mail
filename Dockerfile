FROM python:3.10-alpine
LABEL authors="Red"
WORKDIR '/app'

COPY requirements.txt /tmp/requirements.txt

COPY redttg_mail_backend ./redttg_mail_backend
COPY manage.py .
COPY entrypoint.sh .
COPY run.sh .
COPY wait-for-it.sh .

RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev gcc linux-headers bash

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

# consistent folders for data
RUN mkdir /tmp/files

# enable the entry file for execution
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/run.sh
RUN chmod +x /app/wait-for-it.sh

ENV DJANGO_SETTINGS_MODULE=redttg_mail_backend.settings
ENV DEBUG=0

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]