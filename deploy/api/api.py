import os, time, logging
from typing import List
from routines.routines import Routine, DeployRoutine, StatisticsRoutine, CheckRunningRoutine

SLEEP_SCAN_ROUTINE = int(os.environ["SLEEP_SCAN_ROUTINE"])

def setup_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(level)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)
    return l    

class ServiceApi():
    def __init__(self) -> None:
        self.routines: List[Routine] = []
        self.logger = None
        self._subscribe()
        self._config()

    def _subscribe(self):
        self.routines = [
            DeployRoutine(),
            StatisticsRoutine(),
            CheckRunningRoutine()
        ]
    
    def _config(self):
        self.logger = setup_logger(logger_name='log', log_file='logs.log')

    def start(self) -> None:
        self.logger.info("Scanning routines...")
        loop = 100
        for _ in range(0, loop):
            for routine in self.routines:
                if not routine.running:
                    self.logger.info("{} is not running".format(routine.name))
                    if routine.last_error != '':
                        self.logger.error(routine.last_error)
                        self.logger.error(routine.last_traceback)
                    routine.start()
            time.sleep(SLEEP_SCAN_ROUTINE)
        self.start()
