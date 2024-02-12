FROM python:alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
ONBUILD CMD ["python", "./manage.py shell -c 'from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')'"]
COPY . /code/