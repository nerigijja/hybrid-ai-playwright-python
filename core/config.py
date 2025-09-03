import yaml, pathlib, os, logging

class Config:
    def __init__(self, path: str | None = None):
        p = pathlib.Path(path or 'config/config.yaml')
        with p.open('r', encoding='utf-8') as f:
            self.raw = yaml.safe_load(f)
    def get(self, *keys, default=None):
        cur = self.raw
        for k in keys:
            if isinstance(cur, dict) and k in cur:
                cur = cur[k]
            else:
                return default
        return cur
    
    def load_config(path='config/config.yaml'):
        if os.path.exists(path):
            with open(path) as f:
                return yaml.safe_load(f)
        return {}
  
    @property
    def base_url(self): return self.get('base_url')
