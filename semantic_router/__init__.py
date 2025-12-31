from .route import Route
from .router import SemanticRouter
from .samples import summary_samples, study_samples, chat_samples

semantic_router = SemanticRouter(
    routes=[
        Route(name="study", samples=study_samples),
        Route(name="chat", samples=chat_samples),
        Route(name="summary", samples=summary_samples),
    ]
)
__all__ = [
    'Route',
    'SemanticRouter',
    'summary_samples',
    'study_samples',
    'chat_samples',]