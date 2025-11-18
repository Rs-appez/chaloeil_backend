python manage.py crontab add && \
gunicorn --bind :8000 --workers 2 chaloeil_backend.wsgi
