
import subprocess
import tempfile
import os
import resource

class CodeRunner:
    def __init__(self, cpu_limit=5, memory_limit_mb=256, timeout=8):
        """
        Initialize CodeRunner with configurable resource limits.
        
        Args:
            cpu_limit: CPU time limit in seconds (default: 5)
            memory_limit_mb: Memory limit in MB (default: 256)
            timeout: Process timeout in seconds (default: 8)
        """
        self.cpu_limit = cpu_limit
        self.memory_limit_mb = memory_limit_mb
        self.timeout = timeout
    def run_code(self, code: str):
        """
        Execute Python code in a temporary file with resource limits.
        """
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w') as f:
                f.write(code)
                temp_path = f.name

            def set_limits():
                # Use configurable limits
                resource.setrlimit(resource.RLIMIT_CPU, (self.cpu_limit, self.cpu_limit))
                memory_bytes = self.memory_limit_mb * 1024 * 1024
                resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))

            result = subprocess.run(
                ["python3", temp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout,
                preexec_fn=set_limits
            )
            stdout = result.stdout.decode(errors='replace')
            stderr = result.stderr.decode(errors='replace')
            return stdout, stderr, result.returncode

        except subprocess.TimeoutExpired:
            return "", f"[Execution Error] Code execution timed out after {self.timeout} seconds", -1
        except Exception as e:
            return "", f"[Execution Error] {e}", -1
        finally:
            # Always cleanup temp file
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass  # Best effort cleanup
