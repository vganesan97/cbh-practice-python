from enum import Enum


class JobStatus(Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"


class Job:
    def __init__(self, payload):
        self.payload = payload
        self.status = JobStatus.QUEUED.value
        self.id = id(self)


class Worker:
    def __init__(self):
        self.q = list()
        self.id = id(self)
        self.completed_jobs = list()
        self.running_jobs = list()

    def run_jobs(self):
        while self.q:
            job = self.q.pop(0)
            self.change_job_status(job, JobStatus.RUNNING)
            self.process(job)

    def process(self, job):
        # do some job processing
        print(job.payload)
        self.completed_jobs.append(job)
        self.change_job_status(job, JobStatus.COMPLETED)

    @staticmethod
    def change_job_status(job, status):
        job.status = status.value


class JobScheduler:
    def __init__(self):
        self.workers = list()
        self.worker_cap = 5

    def add_job(self, job):
        if not self.workers:
            self.add_worker()
        for worker in self.workers:
            if len(worker.q) < self.worker_cap:
                worker.q.append(job)
                break

    def add_worker(self):
        worker = Worker()
        self.workers.append(worker)

    def get_queued_jobs(self):
        qjobs = list()
        for worker in self.workers:
            if worker.q:
                qjobs += worker.q
        return qjobs

    def get_running_jobs(self):
        running_jobs = list()
        for worker in self.workers:
            if worker.running_jobs:
                running_jobs += worker.running_jobs
        return running_jobs

    def get_completed_jobs(self):
        completed_jobs = list()
        for worker in self.workers:
            if worker.completed_jobs:
                completed_jobs += worker.completed_jobs
        return completed_jobs
