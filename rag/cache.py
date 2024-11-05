import hashlib

class ResponseCache:
    def __init__(self):
        self.cache = {}
    
    def generate_cache_key(self, query):
        return hashlib.sha256(query.encode('utf-8')).hexdigest()
    
    def get(self, query):
        key = self.generate_cache_key(query)
        return self.cache.get(key, None)
    
    def set(self, query, response):
        key = self.generate_cache_key(query)
        self.cache[key] = response
