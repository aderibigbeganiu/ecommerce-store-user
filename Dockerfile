FROM python:3.8-slim
LABEL maintainer="aderibigbeganiu@gmail.com"
ENV PROJECT_ROOT /usr/src/ecommerce-store-user
WORKDIR $PROJECT_ROOT
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
# CMD python manage.py runserver
CMD ["gunicorn", "--workers", "3", "backend.wsgi:application"]