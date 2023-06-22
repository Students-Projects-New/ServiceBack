from threading import Thread
import uuid

class Worker():
    def __init__(self, guid: str, thread: Thread, delegate: any) -> None:
        self.guid = guid
        self._thread = thread
        self._delegate = delegate
    
    def run(self):
        self._thread.start()
    
    def finish(self):
        self._delegate(self.guid)

class ManageWorker():
    def __init__(self, max_workers: int) -> None:
        self.workers = {}
        self.max_workers = max_workers

    def queue(self, target: any, kwargs: dict) -> Worker:
        guid = str(uuid.uuid4())
        return self._queue(guid=guid, target=target, kwargs=kwargs)

    def _queue(self, guid: str, target: any, kwargs: dict) -> Worker:
        th = Thread(target=target, kwargs=kwargs)
        worker = Worker(guid, th, self.finish)

        self.workers[worker.guid] = worker
        worker.run()
        return worker

    def finish(self, guid: str):
        if guid in self.workers:
            del self.workers[guid]

    def isAvaibleSlot(self) -> bool:
        return len(self.workers.keys()) < self.max_workers

