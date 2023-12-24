FROM python:latest

COPY . .
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["sh", "-c", "if [ \"$SERVER\" = \"asgi\" ]; then uvicorn asgi:app --host 0.0.0.0 --port 8080; else uwsgi --http 0.0.0.0:8080 --module wsgi:app; fi"]