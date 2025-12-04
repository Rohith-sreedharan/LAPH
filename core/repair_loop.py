
import os
from core.llm_interface import LLMInterface
from core.runner import CodeRunner
from core.prompt_manager import PromptManager
from core.logger import Logger

class RepairLoop:
    def __init__(self, model_name="qwen3:14b"):
        self.llm = LLMInterface(model_name)
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
            prompt = self.prompts.build(task, code, last_error)
            code = self.llm.generate(prompt)

            self.logger.log(f"=== Iteration {i+1} ===")
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
