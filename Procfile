web: daphne simple_chat.asgi:application --port $PORT --bind 0.0.0.0 -v2
chatworker: python manage.py runworker --settings=simple_chat.settings -v2