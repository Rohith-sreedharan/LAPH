import re

class CodeSanitizer:
    """
    Analyzes generated code for potentially dangerous operations.
    This is NOT a complete security solution but catches obvious issues.
    """
    
    # Patterns that indicate potentially dangerous operations
    DANGEROUS_PATTERNS = [
        (r'\bos\.system\s*\(', 'os.system() - arbitrary command execution'),
        (r'\beval\s*\(', 'eval() - arbitrary code execution'),
        (r'\bexec\s*\(', 'exec() - arbitrary code execution'),
        (r'\b__import__\s*\(', '__import__() - dynamic imports'),
        (r'\bopen\s*\([^)]*["\']w["\']', 'open() with write mode - file writing'),
        (r'\bopen\s*\([^)]*["\']a["\']', 'open() with append mode - file writing'),
        (r'\bos\.remove\s*\(', 'os.remove() - file deletion'),
        (r'\bos\.rmdir\s*\(', 'os.rmdir() - directory deletion'),
        (r'\bshutil\.rmtree\s*\(', 'shutil.rmtree() - recursive deletion'),
        (r'\bsubprocess\.(run|call|Popen)', 'subprocess - command execution'),
        (r'\bsocket\.', 'socket - network operations'),
        (r'\burllib\.request', 'urllib.request - network operations'),
        (r'\brequests\.', 'requests - network operations'),
    ]
    
    @staticmethod
    def analyze(code: str) -> tuple[list[str], list[str]]:
        """
        Analyze code for potentially dangerous operations.
        
        Args:
            code: Python code to analyze
            
        Returns:
            (warnings, errors) - Lists of warning and error messages
        """
        warnings = []
        errors = []
        
        # Check for dangerous patterns
        for pattern, description in CodeSanitizer.DANGEROUS_PATTERNS:
            if re.search(pattern, code):
                warnings.append(f"Potentially dangerous operation detected: {description}")
        
        # Check for very long code (possible DoS)
        if len(code) > 50000:
            warnings.append("Generated code is very long (>50KB)")
        
        # Check for excessive loops (heuristic)
        loop_count = len(re.findall(r'\b(for|while)\b', code))
        if loop_count > 20:
            warnings.append(f"Code contains many loops ({loop_count}) - potential performance issue")
        
        return warnings, errors
    
    @staticmethod
    def is_safe_for_auto_execution(code: str, allow_file_ops=False, allow_network=False) -> tuple[bool, list[str]]:
        """
        Determine if code is safe enough for automatic execution.
        
        Args:
            code: Code to check
            allow_file_ops: Whether to allow file operations
            allow_network: Whether to allow network operations
            
        Returns:
            (is_safe, reasons) - Whether code is safe and list of reasons if not
        """
        warnings, errors = CodeSanitizer.analyze(code)
        
        unsafe_reasons = []
        
        # Check for absolute no-go operations
        dangerous_ops = ['eval(', 'exec(', 'os.system(', '__import__']
        for op in dangerous_ops:
            if op in code:
                unsafe_reasons.append(f"Code contains {op} which is not allowed for auto-execution")
        
        if not allow_file_ops:
            file_ops = ['open(', 'os.remove', 'os.rmdir', 'shutil.rmtree']
            for op in file_ops:
                if op in code:
                    unsafe_reasons.append(f"Code contains file operation {op} which is not allowed")
        
        if not allow_network:
            network_ops = ['socket.', 'urllib.request', 'requests.']
            for op in network_ops:
                if op in code:
                    unsafe_reasons.append(f"Code contains network operation {op} which is not allowed")
        
        return len(unsafe_reasons) == 0, unsafe_reasons
