
class PromptManager:
    def __init__(self):
        self.prompts = {}
        self.prompts['thinker'] = self._load_prompt('prompts/thinker_prompt.txt')
        self.prompts['summariser'] = self._load_prompt('prompts/summariser_prompt.txt')
        self.prompts['vision'] = self._load_prompt('prompts/vision_prompt.txt')
        self.prompts['coder'] = self._load_prompt('prompts/coder_prompt.txt')

    def _load_prompt(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {path}. Please ensure all prompt files exist.")
        except Exception as e:
            raise RuntimeError(f"Error loading prompt from {path}: {e}")

    def build_thinker(self, task, code=None, error=None):
        return self.prompts['thinker'] + f"\n\nTask: {task}\n" + (f"Previous code: {code}\n" if code else "") + (f"Error: {error}\n" if error else "")

    def build_coder(self, spec, code=None, error=None):
        return self.prompts['coder'] + f"\n\nSpecification: {spec}\n" + (f"Previous code: {code}\n" if code else "") + (f"Error: {error}\n" if error else "")

    def build_summariser(self, logs):
        return self.prompts['summariser'] + f"\n\nLogs: {logs}\n"

    def build_vision(self, description):
        return self.prompts['vision'] + f"\n\nDescription: {description}\n"
