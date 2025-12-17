import unittest
from core.code_extractor import CodeExtractor


class TestCodeExtractor(unittest.TestCase):
    
    def test_extract_markdown_python_block(self):
        """Test extraction of code from ```python blocks"""
        text = """Here is the code you requested:

```python
import os
print("Hello World")
```

This should work fine."""
        
        result = CodeExtractor.extract_code(text)
        self.assertIn("import os", result)
        self.assertIn("print", result)
        self.assertNotIn("Here is", result)
    
    def test_extract_generic_markdown_block(self):
        """Test extraction of code from generic ``` blocks"""
        text = """
```
def hello():
    return "world"
```
"""
        result = CodeExtractor.extract_code(text)
        self.assertIn("def hello", result)
    
    def test_extract_plain_code(self):
        """Test extraction when no markdown blocks present"""
        text = """import sys
def main():
    print("test")

if __name__ == "__main__":
    main()
"""
        result = CodeExtractor.extract_code(text)
        self.assertIn("import sys", result)
        self.assertIn("def main", result)
    
    def test_extract_code_with_explanations(self):
        """Test that explanatory text is filtered out"""
        text = """Here's what I'll do:
import tkinter as tk

def create_window():
    root = tk.Tk()
    return root

This creates a simple window."""
        
        result = CodeExtractor.extract_code(text)
        self.assertIn("import tkinter", result)
        self.assertIn("def create_window", result)
    
    def test_validate_valid_code(self):
        """Test validation of syntactically correct code"""
        code = "import os\nprint('test')"
        is_valid, msg = CodeExtractor.validate_code(code)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_validate_invalid_syntax(self):
        """Test validation catches syntax errors"""
        code = "def broken(\nprint('oops')"
        is_valid, msg = CodeExtractor.validate_code(code)
        self.assertFalse(is_valid)
        self.assertIn("Syntax error", msg)
    
    def test_validate_empty_code(self):
        """Test validation rejects empty code"""
        is_valid, msg = CodeExtractor.validate_code("")
        self.assertFalse(is_valid)
        self.assertIn("Empty", msg)
    
    def test_extract_multiple_blocks_returns_longest(self):
        """Test that longest code block is returned when multiple exist"""
        text = """
```python
import os
```

And here's the full version:

```python
import os
import sys

def main():
    print("Full version")
    return True
```
"""
        result = CodeExtractor.extract_code(text)
        self.assertIn("def main", result)
        self.assertIn("Full version", result)


if __name__ == "__main__":
    unittest.main()
