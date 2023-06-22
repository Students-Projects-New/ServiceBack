import os
from enum import Enum
from database.entities import JobDTO, JobDAO, Status, ProjectDAO
from routines.utils import AESCipher
from workers.workers import Worker

class ServiceType(Enum):
    NONE = 0
    DEPLOY = 1
    LOG = 2
    OFF = 3
    DELETE = 4

    def __str__(self) -> str:
        return self.name

    def get(typeService: str) -> 'ServiceType':
        if typeService == str(ServiceType.DEPLOY.name):
            return ServiceType.DEPLOY
        return ServiceType.NONE

class DeployService():
    def __init__(self, job: JobDTO):
        super().__init__()
        self.context = job.dinamico['context']
        self.port_container = job.dinamico['port_container']
        self.url = job.dinamico['url']
        self.static_path = job.dinamico['static_path']
        dict_var_tmp: dict = job.dinamico['env_var']
        self.job = job
        self.worker: Worker = None

        aes = AESCipher(os.environ["KEY_CRYPT"])
        self.dict_var = {
            k: aes.decrypt(v.encode('ascii'))
            for k, v in dict_var_tmp.items()
        } 
        self.dict_var["DBP_HOST"] = os.environ["DBP_HOST"]
        self.dict_var["DBP_PORT"] = os.environ["DBP_PORT"]
        self.dict_var["DBM_HOST"] = os.environ["DBM_HOST"]
        self.dict_var["DBM_PORT"] = os.environ["DBM_PORT"]
    
    def update_status(self, data: any):
        if self._on_error(data):
            return

        if data['stage'] == 1:
            commit = data['data']['commit']
            ProjectDAO.update_commit_deploy(commit=commit, guid=self.job.guid)

        if data['stage'] == 5:
            ProjectDAO.update_status_project(running=True, status=Status.PRO.value, guid=self.job.guid)

        self.job.message = data["message"]
        self.job.progress = data["progress"]
        self.job.status = Status.PRO.value if data["progress"] == 100 else Status.RUN.value
        self._try_finish(data["progress"])
        
        JobDAO.update_job(self.job)

    def _on_error(self, data: any) -> bool:
        if data["error"] != '':
            self.job.message = data["error"]
            self.job.status = Status.ERR.value
            self.job.progress = data["progress"]
            self._try_finish()
            JobDAO.update_job(self.job)
            ProjectDAO.update_status_project(running= False, status=Status.ERR.value, guid=self.job.guid)
            return True
        return False
    
    def _try_finish(self, progress: int = 100):
        if progress == 100:
            self.worker.finish()

    def kwargs(self) -> dict:
        return {
            'context': self.context,
            'port_container': self.port_container,
            'url': self.url,
            'static_path': self.static_path,
            'env_var': self.dict_var,
            'delegate': self.update_status
        }
