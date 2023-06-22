import daemon, os
from dotenv import load_dotenv

load_dotenv('./.env')

from api.api import ServiceApi
environment = os.environ["ENVIRONMENT"]

def run():
    if environment == "production":
        with daemon.DaemonContext():
            serviceApi = ServiceApi()
            serviceApi.start()
    else:
        serviceApi = ServiceApi()
        serviceApi.start()

if __name__ == '__main__':
    run()