from rag_module.config import EMBED_MODEL
from .base_semantic_router import BaseSemanticRouter
from .samples import DOC_ROUTES, INTENT_ROUTES




class DocRouter(BaseSemanticRouter):
    def __init__(self):
        super().__init__(DOC_ROUTES, reducer="max")
class IntentRouter(BaseSemanticRouter):
    def __init__(self):
        super().__init__(INTENT_ROUTES, reducer="mean")

