from .samples import DOC_ROUTES, INTENT_ROUTES
from rag_module.config import SAMPLES_CACHE_PATH
import pickle
import os





class SampleCache():
    def __init__(self, sample_path):
        self.sample_path = sample_path
    def load_or_build(self):
        if os.path.exists(self.sample_path):
            with open(self.sample_path, 'rb') as f:
                return pickle.load(f)
        
        else:
            data = {
                "doc_routes": DOC_ROUTES,
                "intent_routes": INTENT_ROUTES,
            }
            with open(self.sample_path, 'wb') as f:
                pickle.dump(data, f)
            return data

def load_or_build_samples():
    return SampleCache(SAMPLES_CACHE_PATH).load_or_build()