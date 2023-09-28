release: python manage.py migrate
web: daphne simple_chat.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=simple_chat.settings -v2