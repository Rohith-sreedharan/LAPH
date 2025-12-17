import unittest
from core.code_sanitizer import CodeSanitizer


class TestCodeSanitizer(unittest.TestCase):
    
    def test_safe_code_passes(self):
        """Test that safe code is recognized"""
        code = """
import math

def calculate(x):
    return math.sqrt(x * 2)

print(calculate(10))
"""
        warnings, errors = CodeSanitizer.analyze(code)
        self.assertEqual(len(errors), 0)
    
    def test_eval_detected(self):
        """Test that eval() is detected"""
        code = "result = eval(user_input)"
        warnings, errors = CodeSanitizer.analyze(code)
        self.assertTrue(any('eval()' in w for w in warnings))
    
    def test_exec_detected(self):
        """Test that exec() is detected"""
        code = "exec('print(1)')"
        warnings, errors = CodeSanitizer.analyze(code)
        self.assertTrue(any('exec()' in w for w in warnings))
    
    def test_os_system_detected(self):
        """Test that os.system() is detected"""
        code = "import os\nos.system('rm -rf /')"
        warnings, errors = CodeSanitizer.analyze(code)
        self.assertTrue(any('os.system()' in w for w in warnings))
    
    def test_file_write_detected(self):
        """Test that file write operations are detected"""
        code = "with open('test.txt', 'w') as f:\n    f.write('test')"
        warnings, errors = CodeSanitizer.analyze(code)
        self.assertTrue(any('write mode' in w for w in warnings))
    
    def test_network_operations_detected(self):
        """Test that network operations are detected"""
        code = "import requests\nrequests.get('http://example.com')"
        warnings, errors = CodeSanitizer.analyze(code)
        self.assertTrue(any('network' in w.lower() for w in warnings))
    
    def test_subprocess_detected(self):
        """Test that subprocess is detected"""
        code = "import subprocess\nsubprocess.run(['ls', '-la'])"
        warnings, errors = CodeSanitizer.analyze(code)
        self.assertTrue(any('subprocess' in w for w in warnings))
    
    def test_safe_for_auto_execution(self):
        """Test is_safe_for_auto_execution with safe code"""
        code = "print('Hello World')"
        is_safe, reasons = CodeSanitizer.is_safe_for_auto_execution(code)
        self.assertTrue(is_safe)
        self.assertEqual(len(reasons), 0)
    
    def test_unsafe_eval_for_auto_execution(self):
        """Test is_safe_for_auto_execution rejects eval"""
        code = "eval('1+1')"
        is_safe, reasons = CodeSanitizer.is_safe_for_auto_execution(code)
        self.assertFalse(is_safe)
        self.assertTrue(any('eval(' in r for r in reasons))
    
    def test_file_ops_with_permission(self):
        """Test file operations are allowed when permitted"""
        code = "with open('test.txt', 'w') as f:\n    f.write('test')"
        is_safe, reasons = CodeSanitizer.is_safe_for_auto_execution(code, allow_file_ops=True)
        # File ops should be allowed but still may be unsafe due to other factors
        # The key is that file operations aren't the reason for rejection
        self.assertTrue(all('file operation' not in r for r in reasons))
    
    def test_network_ops_with_permission(self):
        """Test network operations are allowed when permitted"""
        code = "import requests\nrequests.get('http://example.com')"
        is_safe, reasons = CodeSanitizer.is_safe_for_auto_execution(code, allow_network=True)
        # Network ops should be allowed
        self.assertTrue(all('network operation' not in r for r in reasons))


if __name__ == "__main__":
    unittest.main()
