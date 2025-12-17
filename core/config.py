import toml
import os

class Config:
    """
    Configuration manager for LAPH.
    Loads configuration from TOML files with sensible defaults.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.execution_config = self._load_execution_config()
        self.models_config = self._load_models_config()
    
    def _load_execution_config(self):
        """Load execution configuration with defaults"""
        defaults = {
            'resource_limits': {
                'cpu_limit': 5,
                'memory_limit_mb': 256,
                'timeout': 8
            },
            'retry': {
                'initial_delay': 1,
                'max_delay': 10,
                'exponential_backoff': True
            },
            'llm': {
                'request_timeout': 300,
                'connection_pooling': True
            }
        }
        
        try:
            config_path = 'configs/execution.toml'
            if os.path.exists(config_path):
                loaded = toml.load(config_path)
                # Merge with defaults
                for key in defaults:
                    if key in loaded:
                        defaults[key].update(loaded[key])
                return defaults
        except Exception:
            pass
        
        return defaults
    
    def _load_models_config(self):
        """Load models configuration with defaults"""
        defaults = {
            'default': {'name': 'qwen3:14b', 'provider': 'ollama'},
            'mini': {'name': 'qwen3:4b', 'provider': 'ollama'},
            'vision': {'name': 'qwen3-vl:8b', 'provider': 'ollama'},
            'coder': {'name': 'qwen2.5-coder:7b-instruct', 'provider': 'ollama'}
        }
        
        try:
            config_path = 'configs/models.toml'
            if os.path.exists(config_path):
                return toml.load(config_path)
        except Exception:
            pass
        
        return defaults
    
    def get_resource_limits(self):
        """Get resource limits for code execution"""
        return self.execution_config['resource_limits']
    
    def get_retry_config(self):
        """Get retry configuration"""
        return self.execution_config['retry']
    
    def get_llm_config(self):
        """Get LLM configuration"""
        return self.execution_config['llm']
    
    def get_model_config(self, model_type):
        """Get configuration for a specific model type"""
        return self.models_config.get(model_type, self.models_config['default'])
