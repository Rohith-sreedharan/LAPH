
import subprocess
import tempfile
import os
import resource

class CodeRunner:
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
                # Limit CPU time to 5 seconds
                resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
                # Limit memory to 256MB
                resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))

            result = subprocess.run(
                ["python3", temp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=8,
                preexec_fn=set_limits
            )
            stdout = result.stdout.decode(errors='replace')
            stderr = result.stderr.decode(errors='replace')
            return stdout, stderr, result.returncode

        except subprocess.TimeoutExpired:
            return "", "[Execution Error] Code execution timed out after 8 seconds", -1
        except Exception as e:
            return "", f"[Execution Error] {e}", -1
        finally:
            # Always cleanup temp file
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass  # Best effort cleanup
