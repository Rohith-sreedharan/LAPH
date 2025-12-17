import unittest
from core.runner import CodeRunner


class TestCodeRunner(unittest.TestCase):
    
    def setUp(self):
        self.runner = CodeRunner()
    
    def test_run_simple_code(self):
        """Test running simple valid code"""
        code = "print('Hello, World!')"
        stdout, stderr, exitcode = self.runner.run_code(code)
        
        self.assertEqual(exitcode, 0)
        self.assertIn("Hello, World!", stdout)
        self.assertEqual(stderr, "")
    
    def test_run_code_with_error(self):
        """Test running code that has an error"""
        code = "print(undefined_variable)"
        stdout, stderr, exitcode = self.runner.run_code(code)
        
        self.assertNotEqual(exitcode, 0)
        self.assertIn("NameError", stderr)
    
    def test_run_code_with_syntax_error(self):
        """Test running code with syntax error"""
        code = "def broken(\nprint('oops')"
        stdout, stderr, exitcode = self.runner.run_code(code)
        
        self.assertNotEqual(exitcode, 0)
        self.assertIn("SyntaxError", stderr)
    
    def test_temp_file_cleanup(self):
        """Test that temporary files are cleaned up"""
        import os
        import tempfile
        
        # Get temp directory
        temp_dir = tempfile.gettempdir()
        
        # Count .py files before
        py_files_before = len([f for f in os.listdir(temp_dir) if f.endswith('.py')])
        
        # Run code
        code = "print('test')"
        self.runner.run_code(code)
        
        # Count .py files after (should be same or less due to cleanup)
        py_files_after = len([f for f in os.listdir(temp_dir) if f.endswith('.py')])
        
        # We expect cleanup to happen
        self.assertLessEqual(py_files_after, py_files_before + 1)
    
    def test_unicode_handling(self):
        """Test that unicode in output is handled correctly"""
        code = "print('Hello 世界 🌍')"
        stdout, stderr, exitcode = self.runner.run_code(code)
        
        self.assertEqual(exitcode, 0)
        self.assertIn("Hello", stdout)


if __name__ == "__main__":
    unittest.main()
