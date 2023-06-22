#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

def main():
    load_dotenv('./.env')

    file_config = "sp_service_projects.settings."
    if os.environ.get('ENVIRONMENT') == 'production':
        file_config += "production"
    else:
        file_config += "development"
   
    print("Estoy corriendo en %s" % file_config)
    """Run administrative tasks."""
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', file_config)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
