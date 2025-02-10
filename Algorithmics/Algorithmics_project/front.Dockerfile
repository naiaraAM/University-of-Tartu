FROM python:3.11-alpine as base

WORKDIR /code
COPY front front

WORKDIR /code/front

RUN pip install -r req.txt

EXPOSE 3000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:3000"]