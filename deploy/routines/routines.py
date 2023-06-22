import os, time, traceback
from typing import List, Dict, Tuple
from threading import Thread
from workers.workers import ManageWorker
from api.services import DeployService
from database.entities import JobDAO, TypeJob, StatisticsDTO, ProjectDAO, Status
from docker_app.automatization import deploy, get_statistics, container_is_dead

MANAGE_WORKER = ManageWorker(int(os.environ["MAX_WORKERS"]))
SLEEP_DEPLOY_ROUTINE = int(os.environ["SLEEP_DEPLOY_ROUTINE"])
SLEEP_SCAN_STATISTICS = int(os.environ["SLEEP_SCAN_STATISTICS"])
SLEEP_SCAN_CHECK_RUNNING = int(os.environ["SLEEP_SCAN_CHECK_RUNNING"])

class Routine():
    def __init__(self) -> None:
        self.name = 'Routine'
        self.running = False
        self.last_error = ''
        self.last_traceback = ''
    
    def start(self):
        pass

class DeployRoutine(Routine):
    def __init__(self) -> None:
        super().__init__()
        self.name = "DeployRoutine"
        self.pending_jobs = []

    def start(self):
        th = Thread(target=self._start)
        th.start()
        self.running = True
        self.last_error = ''
        self.last_traceback = ''

    def _start(self):
        try:
            if len(self.pending_jobs) == 0:
                self.pending_jobs = JobDAO.get_pending_jobs(TypeJob.DEPLOY.value)

            while MANAGE_WORKER.isAvaibleSlot() and len(self.pending_jobs) > 0:
                job = self.pending_jobs.pop()
                job.status = Status.RUN.value
                JobDAO.update_status_job(job=job)

                service = DeployService(job=job)
                service.worker = MANAGE_WORKER.queue(deploy, service.kwargs())

            time.sleep(SLEEP_DEPLOY_ROUTINE)
            self._start()
        except Exception as e:
            self.running = False
            self.last_error = str(e)
            self.last_traceback = traceback.format_exc()

class StatisticsRoutine(Routine):
    def __init__(self) -> None:
        super().__init__()
        self.name = "StatisticsRoutine"

    def start(self):
        th = Thread(target=self._start)
        th.start()
        self.running = True
        self.last_error = ''
        self.last_traceback = ''

    def _scan_statistics(self):
        ls_statistics: List[Dict] = get_statistics()
        for statistics in ls_statistics:
            self._clean_and_save_data(statistics=statistics)
    
    def _clean_and_save_data(self, statistics: Dict) -> None:
        block_io_res = statistics['BlockIO']#split
        cpu_res = statistics['CPUPerc']     #perc
        mem_perc_res = statistics['MemPerc']#perc
        mem_res = statistics['MemUsage']    #split
        net_io_res = statistics['NetIO']    #split
        context_res = statistics['Name']    #str

        statistics_dto = StatisticsDTO()
        statistics_dto.block_io_usage, statistics_dto.block_io_assign = self._get_pair_value(block_io_res)
        statistics_dto.mem_usage, statistics_dto.mem_assign = self._get_pair_value(mem_res)
        statistics_dto.net_io_usage, statistics_dto.net_io_assign = self._get_pair_value(net_io_res)
        statistics_dto.cpu_perc = self._get_removed_percent(cpu_res)
        statistics_dto.mem_perc = self._get_removed_percent(mem_perc_res)
        statistics_dto.context = context_res

        ProjectDAO.update_statistics_project(statistics=statistics_dto)

    def _get_pair_value(self, value: str) -> Tuple[str, str]:
        return value.replace(' ', '').split('/')

    def _get_removed_percent(self, value: str) -> float:
        return float(value.replace('%', ''))

    def _start(self):
        try:
            self._scan_statistics()
            time.sleep(SLEEP_SCAN_STATISTICS)
            self._start()
        except Exception as e:
            self.running = False
            self.last_error = str(e)
            self.last_traceback = traceback.format_exc()

class CheckRunningRoutine(Routine):
    def __init__(self) -> None:
        super().__init__()
        self.name = "CheckRunningRoutine"

    def start(self):
        th = Thread(target=self._start)
        th.start()
        self.running = True
        self.last_error = ''
        self.last_traceback = ''
    
    def _scan_projects(self):
        projects = ProjectDAO.get_projects_running()
        for project in projects:
            if container_is_dead(project.context):
                project.running = False
                ProjectDAO.update_running_project(project=project)

    def _start(self):
        try:
            self._scan_projects()
            time.sleep(SLEEP_SCAN_CHECK_RUNNING)
            self._start()
        except Exception as e:
            self.running = False
            self.last_error = str(e)
            self.last_traceback = traceback.format_exc()
