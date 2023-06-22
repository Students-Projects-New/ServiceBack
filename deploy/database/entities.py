from .connection import PostgresConnector
from typing import List
from enum import Enum
import json
import datetime as dt

class Status(Enum):
    VIG = 'VIG'
    PRO = 'PRO'
    RUN = 'RUN'
    CAN = 'CAN'
    ERR = 'ERR'

class TypeJob(Enum):
    DEPLOY = 'DEPLOY'

class JobDTO():
    def __init__(self) -> None:
        self.id: int = 0
        self.guid: str = ""
        self.dinamico: str = ""
        self.message: str = "" 
        self.status: str = ""
        self.progress: int = 0

class StatisticsDTO():
    def __init__(self) -> None:
        self.context: str = ""
        self.cpu_perc: float = 0
        self.mem_perc: float = 0
        self.mem_usage: str = ""
        self.mem_assign: str = ""
        self.block_io_usage: str = ""
        self.block_io_assign: str = ""
        self.net_io_usage: str = ""
        self.net_io_assign: str = ""

class ProjectDTO():
    def __init__(self) -> None:
        self.id: int = 0
        self.context: str = ""
        self.running: bool = False

class JobDAO():
    def get_pending_jobs(type: str) -> List[JobDTO]:
        psql = PostgresConnector()
        _, cur = psql.open()
        cur.execute("""
            SELECT 
                id, 
                guid, 
                dinamico,
                message,
                status,
                progress
            FROM app_project_job 
            WHERE status = '{}' 
                AND type = '{}'
            order by 1 desc
            LIMIT 5;""".format(Status.VIG.value, type))

        ls_jobs = cur.fetchall()
        res_jobs = []
        for job in ls_jobs:
            jobd = JobDTO()
            jobd.id = job[0]
            jobd.guid = job[1]
            jobd.dinamico = json.loads(job[2])
            jobd.message = job[3]
            jobd.status = job[4]
            jobd.progress = job[5]
            res_jobs.append(jobd)

        psql.close()
        return res_jobs
    
    def update_job(job: JobDTO):
        psql = PostgresConnector()
        _, cur = psql.open()
        cur.execute("""
            UPDATE app_project_job
            SET
                message = '{}',
                status = '{}',
                progress = {}
            WHERE id = {};""".format(job.message, job.status, job.progress, job.id))
        psql.close()
    
    def update_status_job(job: JobDTO):
        psql = PostgresConnector()
        _, cur = psql.open()
        cur.execute("""
            UPDATE app_project_job
            SET
                status = '{}'
            WHERE id = {};""".format(job.status, job.id))
        psql.close()

class ProjectDAO():
    def update_commit_deploy(commit: str, guid: str):
        psql = PostgresConnector()
        _, cur = psql.open()
        cur.execute("""
            UPDATE app_project_projectdeploy
            SET
                commit = '{}'
            WHERE guid = '{}';""".format(commit, guid))
        psql.close()

    def update_status_project(running: bool, status: str, guid: str):
        psql = PostgresConnector()
        _, cur = psql.open()
        #Usar contexto transaccional
        cur.execute("""
            UPDATE app_project_project
            SET
                running = {}
            WHERE guid = '{}';""".format(running, guid))

        cur.execute("""
            UPDATE app_project_projectdeploy
            SET
                successful = {},
                status = '{}'
            WHERE guid = '{}';""".format(
                running, status, guid
            ))
        psql.close()
    
    def update_statistics_project(statistics: StatisticsDTO):
        psql = PostgresConnector()
        _, cur = psql.open()
        #Usar contexto transaccional
        cur.execute("""
            SELECT 
                id 
            FROM app_project_project
            WHERE context = '{}'
            """.format(statistics.context))

        project = cur.fetchone()
        if project != None:
            cur.execute("""
                INSERT into app_project_projectstatistics 
                (id_project_id, cpu_perc, mem_perc, mem_usage, mem_assign, block_io_usage, block_io_assign, net_io_usage, net_io_assign, created_at)
                VALUES 
                ({},{},{},'{}','{}','{}','{}','{}','{}', '{}');""".format(
                    project[0],
                    statistics.cpu_perc,
                    statistics.mem_perc,
                    statistics.mem_usage,
                    statistics.mem_assign,
                    statistics.block_io_usage,
                    statistics.block_io_assign,
                    statistics.net_io_usage,
                    statistics.net_io_assign,
                    dt.datetime.now()
                ))
            cur.execute("""
                DELETE FROM app_project_projectstatistics 
                WHERE id NOT IN (SELECT id FROM app_project_projectstatistics WHERE id_project_id = {0} ORDER BY 1 DESC LIMIT 50) 
                AND id_project_id = {0};
                """.format(project[0]))
        psql.close()

    def get_projects_running() -> List[ProjectDTO]:
        psql = PostgresConnector()
        _, cur = psql.open()
        cur.execute("""
            SELECT 
                id,
                context,
                running 
            FROM app_project_project
            WHERE running = {}
            """.format(True))

        ls_projects = cur.fetchall()
        res: List[ProjectDTO] = []
        for _project in ls_projects:
            project = ProjectDTO()
            project.id = _project[0]
            project.context = _project[1]
            project.running = _project[2]
            res.append(project)
        
        psql.close()

        return res
    
    def update_running_project(project: ProjectDTO):
        psql = PostgresConnector()
        _, cur = psql.open()
        cur.execute("""
            UPDATE app_project_project
            SET
                running = {}
            WHERE id = {};
            """.format(project.running, project.id))
        
        psql.close()