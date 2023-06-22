ps -ef | grep .venv/bin/python  | awk '{print $2}' | xargs kill -9
