mkdir staticfiles -p
python manage.py collectstatic --noinput
python manage.py migrate