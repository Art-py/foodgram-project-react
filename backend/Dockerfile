FROM python:3.7.9
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]