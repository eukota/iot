import json
import logging
import os


class ConfigLoader:
    def __init__(self, config_path=None, secrets_path=None):
        self.config_path = config_path or self.default_config_path()
        self.secrets_path = secrets_path or self.default_secrets_path()
        self._cache = {}

    @staticmethod
    def _config_dir():
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(script_dir, '..', 'config_files'))

    @classmethod
    def default_config_path(cls):
        return os.path.join(cls._config_dir(), 'config.json')

    @classmethod
    def default_secrets_path(cls):
        return os.path.join(cls._config_dir(), 'secrets.json')

    def load_config(self, force_reload=False):
        return self._load_json(self.config_path, force_reload=force_reload)

    def load_secrets(self, force_reload=False):
        return self._load_json(self.secrets_path, force_reload=force_reload)

    def _load_json(self, path, force_reload=False):
        if not force_reload and path in self._cache:
            return self._cache[path]
        try:
            with open(path, 'r') as f:
                data = json.load(f)
        except Exception as exc:
            logging.error("Failed to load JSON from %s: %s", path, exc)
            data = {}
        self._cache[path] = data
        return data
