python manage.py crontab add && \
python manage.py loaddata level && \
gunicorn --bind :8000 --workers 2 chaloeil_backend.wsgi
