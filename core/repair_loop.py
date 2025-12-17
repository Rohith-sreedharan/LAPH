
import os
import time
from core.llm_interface import LLMInterface
from core.runner import CodeRunner
from core.prompt_manager import PromptManager
from core.logger import Logger
from core.code_extractor import CodeExtractor
from core.code_sanitizer import CodeSanitizer

class RepairLoop:
    def __init__(self, logger: Logger, model_name="qwen3:14b"):
        # Load all models
        import toml
        self.logger = logger
        
        try:
            models_cfg = toml.load("configs/models.toml")
            self.models = {
                'thinker': LLMInterface(models_cfg['mini']['name']),
                'summariser': LLMInterface(models_cfg['mini']['name']),
                'vision': LLMInterface(models_cfg['vision']['name']),
                'coder': LLMInterface(models_cfg['coder']['name'])
            }
        except FileNotFoundError:
            self.logger.log("ERROR: configs/models.toml not found. Using default models.")
            self.models = {
                'thinker': LLMInterface("qwen3:4b"),
                'summariser': LLMInterface("qwen3:4b"),
                'vision': LLMInterface("qwen3-vl:8b"),
                'coder': LLMInterface("qwen2.5-coder:7b-instruct")
            }
        except Exception as e:
            self.logger.log(f"ERROR loading models config: {e}. Using defaults.")
            self.models = {
                'thinker': LLMInterface("qwen3:4b"),
                'summariser': LLMInterface("qwen3:4b"),
                'vision': LLMInterface("qwen3-vl:8b"),
                'coder': LLMInterface("qwen2.5-coder:7b-instruct")
            }
        
        self.runner = CodeRunner()
        try:
            self.prompts = PromptManager()
        except Exception as e:
            self.logger.log(f"ERROR loading prompts: {e}")
            raise

    def _generate_spec(self, task, code, last_error, stream_callback):
        thinker_prompt = self.prompts.build_thinker(task, code, last_error)
        self.logger.log("--- Thinker Prompt ---\n" + thinker_prompt)
        
        # Use list accumulation for better performance
        spec_chunks = []
        self.logger.log("--- Thinker Output ---")
        for chunk in self.models['thinker'].generate(thinker_prompt):
            spec_chunks.append(chunk)
            if stream_callback:
                stream_callback(chunk, "thinker")
        return ''.join(spec_chunks)

    def _generate_code(self, spec, code, last_error, stream_callback):
        coder_prompt = self.prompts.build_coder(spec, code, last_error)
        self.logger.log("--- Coder Prompt ---\n" + coder_prompt)
        
        # Use list accumulation for better performance
        output_chunks = []
        self.logger.log("--- Coder Output ---")
        for chunk in self.models['coder'].generate(coder_prompt):
            output_chunks.append(chunk)
            if stream_callback:
                stream_callback(chunk, "coder")
        
        raw_output = ''.join(output_chunks)
        
        # Extract actual code from LLM response
        extracted_code = CodeExtractor.extract_code(raw_output)
        
        # Validate the extracted code
        is_valid, error_msg = CodeExtractor.validate_code(extracted_code)
        if not is_valid:
            self.logger.log(f"WARNING: Code extraction/validation issue: {error_msg}")
            self.logger.log("Using raw output as fallback.")
            return raw_output
        
        # Analyze code for security issues
        warnings, errors = CodeSanitizer.analyze(extracted_code)
        if warnings:
            self.logger.log("--- Security Analysis Warnings ---")
            for warning in warnings:
                self.logger.log(f"⚠️  {warning}")
        
        self.logger.log("--- Code extracted and validated successfully ---")
        return extracted_code

    def run_task(self, task: str, max_iters=20, stream_callback=None):
        code = None
        last_error = None
        retry_delay = 1  # Start with 1 second delay

        for i in range(max_iters):
            self.logger.log(f"\n{'='*50}")
            self.logger.log(f"Iteration {i+1}/{max_iters}")
            self.logger.log(f"{'='*50}\n")

            try:
                spec = self._generate_spec(task, code, last_error, stream_callback)
                
                # Check if LLM returned an error
                if "[LLM ERROR]" in spec:
                    self.logger.log(f"LLM error detected. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, 10)  # Exponential backoff, max 10s
                    continue
                
                code = self._generate_code(spec, code, last_error, stream_callback)
                
                # Check if LLM returned an error
                if "[LLM ERROR]" in code:
                    self.logger.log(f"LLM error detected. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, 10)  # Exponential backoff, max 10s
                    continue
                
                # Reset retry delay on success
                retry_delay = 1

                self.logger.log("--- Running Code ---")
                stdout, stderr, exitcode = self.runner.run_code(code)

                self.logger.log("--- Execution Result ---")
                if stdout:
                    self.logger.log(f"STDOUT:\n{stdout}")
                if stderr:
                    self.logger.log(f"STDERR:\n{stderr}")
                self.logger.log(f"Exit Code: {exitcode}")

                if exitcode == 0:
                    self.logger.log("\n🎉 Success! Program runs without errors.")
                    return code

                last_error = stderr
                self.logger.log("\n--- Code failed, trying again... ---")
                time.sleep(2)
                
            except Exception as e:
                self.logger.log(f"ERROR during iteration: {e}")
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 10)

        self.logger.log("\n❌ Failed to generate a working script after max iterations.")
        return None
