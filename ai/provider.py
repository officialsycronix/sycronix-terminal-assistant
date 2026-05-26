import json, httpx, sys, os
if __name__ != "__main__":
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)

from typing import Optional
from sycronix.core.config import get_api_key
from sycronix.core.logging_setup import logger

MODEL = "meta-llama/llama-3.3-70b-instruct:free"
BASE_URL = "https://openrouter.ai/api/v1"

class AIProvider:
    def __init__(self):
        self.api_key = get_api_key()

    def chat(self, messages, system_prompt=None):
        if not self.api_key:
            return False, "API key not configured. Run 'python3 setup_api.py' first."

        if system_prompt:
            full_messages = [{"role": "system", "content": system_prompt}] + messages
        else:
            full_messages = messages

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": MODEL,
            "messages": full_messages,
            "max_tokens": 2048,
        }

        try:
            with httpx.Client(timeout=90.0, follow_redirects=True) as client:
                resp = client.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    content = data["choices"][0]["message"]["content"]
                    return True, content
                else:
                    error = f"API Error ({resp.status_code}): {resp.text[:200]}"
                    logger.error(error)
                    return False, error
        except httpx.TimeoutException:
            return False, "Request timed out. Check your internet connection."
        except Exception as e:
            return False, f"Connection error: {e}"

    def stream_chat(self, messages, system_prompt=None):
        if not self.api_key:
            yield False, "API key not configured."
            return

        if system_prompt:
            full_messages = [{"role": "system", "content": system_prompt}] + messages
        else:
            full_messages = messages

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": MODEL,
            "messages": full_messages,
            "max_tokens": 2048,
            "stream": True,
        }

        try:
            with httpx.Client(timeout=120.0, follow_redirects=True) as client:
                with client.stream("POST", f"{BASE_URL}/chat/completions", headers=headers, json=payload) as resp:
                    if resp.status_code != 200:
                        yield False, f"API Error ({resp.status_code})"
                        return
                    for line in resp.iter_lines():
                        if line.startswith("data: "):
                            data = line[6:]
                            if data.strip() == "[DONE]":
                                break
                            try:
                                chunk = json.loads(data)
                                delta = chunk["choices"][0]["delta"]
                                if "content" in delta:
                                    yield True, delta["content"]
                            except:
                                continue
        except Exception as e:
            yield False, f"Error: {e}"
