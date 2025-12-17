import re

class CodeExtractor:
    """
    Extract actual Python code from LLM responses that may include markdown,
    explanations, or other non-code content.
    """
    
    @staticmethod
    def extract_code(text: str) -> str:
        """
        Extract Python code from text that may contain markdown code blocks or explanations.
        
        Args:
            text: Raw text from LLM that may contain code blocks
            
        Returns:
            Extracted Python code, or original text if no code blocks found
        """
        # Try to find code between ```python and ``` or ``` and ```
        patterns = [
            r'```python\s*\n(.*?)\n```',  # ```python ... ```
            r'```\s*\n(.*?)\n```',         # ``` ... ```
            r'<code>(.*?)</code>',         # <code> ... </code>
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            if matches:
                # Return the longest code block found
                return max(matches, key=len).strip()
        
        # If no code blocks found, try to extract lines that look like code
        # by removing common explanatory prefixes
        lines = text.split('\n')
        code_lines = []
        in_code = False
        
        for line in lines:
            stripped = line.strip()
            
            # Skip obvious non-code lines
            if stripped.startswith(('Here', 'This', 'The', 'I', 'You', 'Let', 'Now', 'First', 'Note:')):
                continue
            
            # Keep lines that look like Python code
            if stripped and (
                stripped.startswith(('import ', 'from ', 'def ', 'class ', 'if ', 'for ', 'while ', '@', '#'))
                or '=' in stripped
                or stripped.startswith(('print(', 'return ', 'yield ', 'raise ', 'try:', 'except'))
                or in_code
            ):
                code_lines.append(line)
                in_code = True
            elif in_code and (stripped == '' or stripped.startswith(' ')):
                # Keep empty lines and indented lines when already in code
                code_lines.append(line)
        
        if code_lines:
            extracted = '\n'.join(code_lines).strip()
            # Only return if it looks like substantial code
            if len(extracted) > 20:
                return extracted
        
        # Last resort: return original text
        return text.strip()
    
    @staticmethod
    def validate_code(code: str) -> tuple[bool, str]:
        """
        Validate that the extracted text is likely valid Python code.
        
        Args:
            code: Code to validate
            
        Returns:
            (is_valid, error_message)
        """
        if not code or not code.strip():
            return False, "Empty code"
        
        # Check for minimum code characteristics
        has_import_or_def = any(keyword in code for keyword in ['import ', 'from ', 'def ', 'class '])
        has_basic_syntax = any(char in code for char in ['(', ')', '='])
        
        if not (has_import_or_def or has_basic_syntax):
            return False, "Does not appear to be valid Python code"
        
        # Try to compile to check for syntax errors
        try:
            compile(code, '<string>', 'exec')
            return True, ""
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        except Exception as e:
            return False, f"Validation error: {e}"
