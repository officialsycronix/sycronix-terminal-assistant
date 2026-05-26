from sycronix.ai.provider import AIProvider
from sycronix.core.config import get_api_key

DEBUG_PROMPT = """You are an expert debugger. Given an error message and the command that produced it:

1. Analyze the root cause
2. Provide the exact fix command(s)
3. Explain what went wrong in one line

Return your response as:
ANALYSIS: <one line explanation>
FIX: <exact command to fix>
FIX_TYPE: <run_command | modify_file | install>

Be precise. Only return the analysis and fix."""

ERROR_PATTERNS = {
    "module not found": {"suggestion": "pip install MODULE_NAME", "fix_type": "install"},
    "no module named": {"suggestion": "pip install PACKAGE_NAME", "fix_type": "install"},
    "command not found": {"suggestion": "pkg install PACKAGE_NAME", "fix_type": "install"},
    "permission denied": {"suggestion": "chmod +x FILE_PATH", "fix_type": "run_command"},
    "port already in use": {"suggestion": "kill $(lsof -ti:PORT) 2>/dev/null", "fix_type": "run_command"},
    "connection refused": {"suggestion": "Check if the service is running", "fix_type": "run_command"},
    "syntaxerror": {"suggestion": "Check syntax in the referenced file", "fix_type": "modify_file"},
    "importerror": {"suggestion": "pip install MISSING_PACKAGE", "fix_type": "install"},
    "file not found": {"suggestion": "Create the missing file or directory", "fix_type": "run_command"},
    "pip: not found": {"suggestion": "pkg install python-pip", "fix_type": "install"},
    "npm: not found": {"suggestion": "pkg install nodejs", "fix_type": "install"},
}


class Debugger:
    def __init__(self):
        self.provider = AIProvider()

    def analyze(self, error_text: str, command: str = "") -> dict:
        error_lower = error_text.lower()

        for pattern, fix_info in ERROR_PATTERNS.items():
            if pattern in error_lower:
                suggestion = fix_info["suggestion"]
                if "MODULE_NAME" in suggestion:
                    for line in error_text.split("\n"):
                        if "no module named" in line.lower():
                            parts = line.lower().split("no module named")
                            if len(parts) > 1:
                                mod = parts[1].strip().strip("'\"")
                                suggestion = suggestion.replace("MODULE_NAME", mod)
                                break
                if "PACKAGE_NAME" in suggestion:
                    for line in error_text.split("\n"):
                        if "module not found" in line.lower() or "no module named" in line.lower() or "not found" in line.lower():
                            parts = line.strip().split()[-1]
                            suggestion = suggestion.replace("PACKAGE_NAME", parts)
                            break
                if "FILE_PATH" in suggestion:
                    for line in error_text.split("\n"):
                        if "permission denied" in line.lower():
                            parts = line.strip().split()[-1]
                            suggestion = suggestion.replace("FILE_PATH", parts)
                            break

                return {
                    "analysis": f"Detected: {pattern}",
                    "fix_command": suggestion,
                    "fix_type": fix_info["fix_type"],
                }

        if get_api_key():
            return self._ai_analyze(error_text, command)
        return {
            "analysis": "Unknown error pattern. Enable API key for AI-powered debugging.",
            "fix_command": "",
            "fix_type": "run_command",
        }

    def _ai_analyze(self, error_text: str, command: str) -> dict:
        ok, response = self.provider.chat(
            [{"role": "user", "content": f"Command: {command}\nError:\n{error_text}"}],
            DEBUG_PROMPT,
        )
        if ok:
            analysis = ""
            fix = ""
            fix_type = "run_command"
            for line in response.split("\n"):
                if line.startswith("ANALYSIS:"):
                    analysis = line[9:].strip()
                elif line.startswith("FIX:"):
                    fix = line[4:].strip()
                elif line.startswith("FIX_TYPE:"):
                    fix_type = line[9:].strip()
            return {
                "analysis": analysis or "AI analysis unavailable",
                "fix_command": fix,
                "fix_type": fix_type,
            }
        return {
            "analysis": "Could not analyze error with AI",
            "fix_command": "",
            "fix_type": "run_command",
        }
