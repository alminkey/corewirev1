from core.db.models.pipeline import PipelineRun


class PipelineRepository:
    def __init__(self, session):
        self.session = session

    def create_run(self, payload: dict) -> PipelineRun:
        run = PipelineRun(**payload)
        self.session.add(run)
        self.session.flush()
        return run
