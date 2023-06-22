sudo .venv/bin/gunicorn --bind localhost:8001 sp_service_academic.wsgi -t 600 --daemon
