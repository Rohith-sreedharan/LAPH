
import requests
import json

class LLMInterface:
    def __init__(self, model_name="qwen3:14b"):
        self.model_name = model_name

    def generate(self, prompt: str, timeout=300):
        """
        Send a prompt to a local Ollama model via HTTP API and stream the output.
        
        Args:
            prompt: The prompt to send to the model
            timeout: Request timeout in seconds (default: 300)
        """
        try:
            url = "http://localhost:11434/api/generate"
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": True
            }
            response = requests.post(url, json=payload, stream=True, timeout=timeout)
            response.raise_for_status()
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        chunk = data.get("response", "")
                        full_response += chunk
                        yield chunk
                    except json.JSONDecodeError:
                        # Ignore lines that are not valid JSON
                        pass
        except requests.exceptions.Timeout:
            yield f"[LLM ERROR] Request timed out after {timeout} seconds"
        except requests.exceptions.ConnectionError:
            yield "[LLM ERROR] Cannot connect to Ollama. Is it running on localhost:11434?"
        except Exception as e:
            yield f"[LLM ERROR] {e}"
