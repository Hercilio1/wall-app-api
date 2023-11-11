FROM python:3.10
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Adds our application code to the image
COPY . code

WORKDIR code

EXPOSE 8000

# Run the production server
CMD ["bash", "-c", "python wait_for_postgres.py", \
    "&& python manage.py migrate", \
    "&& python manage.py collectstatic --noinput", \
    "&& python manage.py create_oauth_app", \
    "&& gunicorn --bind 0.0.0.0:8000 --access-logfile - wall_app_api.wsgi:application"]
