FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ADD Lazapee .
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 80
CMD python manage.py runserver 0.0.0.0:80 OR $PORT