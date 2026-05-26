import json
from sycronix.ai.provider import AIProvider
from sycronix.core.config import get_api_key

PLANNER_PROMPT = """You are an expert software architect and developer. Given a user request, create a detailed plan.

Return ONLY a JSON array of steps. Each step has:
- "name": short action name
- "description": what to do
- "type": one of "create_file", "modify_file", "run_command", "install", "configure"
- "target": the file path or command to run

Example:
[
  {"name": "Create project dir", "description": "Create the project directory structure", "type": "run_command", "target": "mkdir -p myproject/src"},
  {"name": "Install Flask", "description": "Install Flask and dependencies", "type": "install", "target": "pip install flask"},
  {"name": "Create app.py", "description": "Create the main Flask application", "type": "create_file", "target": "myproject/src/app.py"},
  {"name": "Run app", "description": "Start the Flask development server", "type": "run_command", "target": "cd myproject && python src/app.py"}
]

Be specific with commands. Use pip, npm, cargo etc. as appropriate."""


class Planner:
    def __init__(self):
        self.provider = AIProvider()

    def plan(self, request: str) -> list:
        if not get_api_key():
            return self._fallback_plan(request)

        ok, response = self.provider.chat(
            [{"role": "user", "content": request}],
            PLANNER_PROMPT,
        )

        if ok:
            try:
                cleaned = response.strip()
                if cleaned.startswith("```"):
                    cleaned = cleaned.split("\n", 1)[1]
                    cleaned = cleaned.rsplit("\n", 1)[0]
                    if cleaned.endswith("```"):
                        cleaned = cleaned[:-3]
                plan = json.loads(cleaned)
                if isinstance(plan, list):
                    return plan
            except (json.JSONDecodeError, IndexError):
                return self._fallback_plan(request)
        return self._fallback_plan(request)

    def _fallback_plan(self, request: str) -> list:
        request_lower = request.lower()
        if "flask" in request_lower or "web" in request_lower or "app" in request_lower:
            return [
                {"name": "Create project structure", "description": "Create directories", "type": "run_command", "target": "mkdir -p project/src project/templates project/static"},
                {"name": "Create app.py", "description": "Create main application file", "type": "create_file", "target": "project/src/app.py"},
                {"name": "Create requirements", "description": "Create requirements.txt", "type": "create_file", "target": "project/requirements.txt"},
                {"name": "Install dependencies", "description": "Install Python packages", "type": "install", "target": "pip install -r project/requirements.txt"},
                {"name": "Run application", "description": "Start the application", "type": "run_command", "target": "cd project && python src/app.py"},
            ]
        elif "fastapi" in request_lower or "api" in request_lower:
            return [
                {"name": "Create project structure", "description": "Create directories", "type": "run_command", "target": "mkdir -p fastapi_app/app fastapi_app/tests"},
                {"name": "Create main.py", "description": "Create FastAPI main file", "type": "create_file", "target": "fastapi_app/app/main.py"},
                {"name": "Install dependencies", "description": "Install FastAPI and uvicorn", "type": "install", "target": "pip install fastapi uvicorn"},
                {"name": "Run server", "description": "Start FastAPI server", "type": "run_command", "target": "cd fastapi_app && uvicorn app.main:app --reload"},
            ]
        elif "react" in request_lower or "frontend" in request_lower or "portfolio" in request_lower:
            return [
                {"name": "Create React app", "description": "Scaffold React project", "type": "run_command", "target": "npx create-react-app portfolio 2>/dev/null || npm init -y"},
                {"name": "Install dependencies", "description": "Install required packages", "type": "install", "target": "npm install react react-dom"},
                {"name": "Build project", "description": "Build for production", "type": "run_command", "target": "npm run build 2>/dev/null || echo 'No build script'"},
            ]
        elif "python" in request_lower or "cli" in request_lower:
            return [
                {"name": "Create project structure", "description": "Create project layout", "type": "run_command", "target": "mkdir -p python_cli/src python_cli/tests"},
                {"name": "Create main module", "description": "Create the CLI entry point", "type": "create_file", "target": "python_cli/src/main.py"},
                {"name": "Create setup.py", "description": "Package configuration", "type": "create_file", "target": "python_cli/setup.py"},
                {"name": "Test run", "description": "Verify the CLI works", "type": "run_command", "target": "cd python_cli && python src/main.py --help"},
            ]
        else:
            return [
                {"name": "Analyze request", "description": "Understanding requirements", "type": "run_command", "target": f"echo 'Planning: {request}'"},
                {"name": "Create project root", "description": "Set up workspace", "type": "run_command", "target": "mkdir -p project"},
                {"name": "Initialize project", "description": "Add starter files", "type": "create_file", "target": "project/README.md"},
            ]
