from core.db.models.story import StoryAnalysis, StoryCluster


class StoryRepository:
    def __init__(self, session):
        self.session = session

    def create_cluster(self, payload: dict) -> StoryCluster:
        cluster = StoryCluster(**payload)
        self.session.add(cluster)
        self.session.flush()
        return cluster

    def create_analysis(self, payload: dict) -> StoryAnalysis:
        analysis = StoryAnalysis(**payload)
        self.session.add(analysis)
        self.session.flush()
        return analysis
