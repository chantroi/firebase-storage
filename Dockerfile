FROM python:latest

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["uwsgi", "--http", "0.0.0.0:8080", "--module", "wsgi:app"]