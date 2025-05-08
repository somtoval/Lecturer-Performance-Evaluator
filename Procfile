web: gunicorn lecturer_performance.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn lecturer_performance.wsgi