ps -ef | grep /var2/students-project-backend/sp_service_projects/.venv/bin/python3  | awk '{print $2}' | xargs kill -9 || true
