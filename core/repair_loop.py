
import os
from core.llm_interface import LLMInterface
from core.runner import CodeRunner
from core.prompt_manager import PromptManager
from core.logger import Logger

class RepairLoop:
    def __init__(self, model_name="qwen3:14b"):
        # Load all models
        from core.llm_interface import LLMInterface
        import toml
        models_cfg = toml.load("configs/models.toml")
        self.models = {
            'thinker': LLMInterface(models_cfg['default']['name']),
            'summariser': LLMInterface(models_cfg['mini']['name']),
            'vision': LLMInterface(models_cfg['vision']['name']),
            'coder': LLMInterface(models_cfg['coder']['name'])
        }
        self.runner = CodeRunner()
        self.prompts = PromptManager()
        self.logger = Logger()

    def run_task(self, task: str, max_iters=10):
        # Load state if exists
        state_path = "state.txt"
        code = None
        last_error = None
        iteration = 0
        if os.path.exists(state_path):
            with open(state_path, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("iteration:"):
                        iteration = int(line.split(":",1)[1].strip())
                    elif line.startswith("last_code:"):
                        code = line.split(":",1)[1].strip().strip('"')
                    elif line.startswith("last_error:"):
                        last_error = line.split(":",1)[1].strip().strip('"')

        for i in range(iteration, max_iters):
            # 1. Use thinker to generate/refine the specification
            thinker_prompt = self.prompts.build_thinker(task, code, last_error)
            spec = self.models['thinker'].generate(thinker_prompt)

            # 2. Use coder to generate code from the specification
            coder_prompt = self.prompts.build_coder(spec, code, last_error)
            code = self.models['coder'].generate(coder_prompt)

            self.logger.log(f"=== Iteration {i+1} ===")
            self.logger.log("Specification:\n" + spec)
            self.logger.log("Generated code:\n" + code)

            stdout, stderr, exitcode = self.runner.run_code(code)

            self.logger.log("STDOUT:\n" + stdout)
            self.logger.log("STDERR:\n" + stderr)

            # Persist state
            with open(state_path, "w") as f:
                f.write(f"iteration: {i+1}\n")
                f.write(f"last_code: \"{code}\"\n")
                f.write(f"last_error: \"{stderr}\"\n")

            if exitcode == 0:
                print("🎉 Success! Program runs without errors.")
                return code

            last_error = stderr

        print("❌ Failed after max iterations.")
        return None
