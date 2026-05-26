import re
import os
from pathlib import Path
from sycronix.ai.provider import AIProvider
from sycronix.agent.executor import Executor
from sycronix.memory.store import store

AGENT_PROMPT = """You are SYCRONIX DEV AGENT — an autonomous AI developer assistant.

You help users build projects, write code, fix errors, and run commands.

RULES:
- Be conversational and concise
- When creating files, show the content inline in your response
- When the user asks to build something, create real files on disk
- Use MARKDOWN code blocks with filenames like ```filename.py
- After showing code, ask if the user wants to run it
- Keep track of what you've built

To create files, end your file blocks with:
→ CREATE: path/to/file.py
Then show the file content in a code block.

To run commands, say:
→ RUN: command here

Current directory: {cwd}"""


class DevAgent:
    def __init__(self):
        self.provider = AIProvider()
        self.executor = Executor()
        self.active = False
        self.messages = []
        self.conversation_active = False

    def _build_system_prompt(self):
        return AGENT_PROMPT.format(cwd=os.getcwd())

    def _parse_actions(self, text: str):
        actions = []
        create_matches = re.findall(r'→ CREATE:\s*(.+?)(?:\n|$)', text)
        for path in create_matches:
            path = path.strip().strip('`').strip()
            if not os.path.isabs(path):
                path = os.path.join(os.getcwd(), path)
            actions.append({"type": "create", "target": path})
        run_matches = re.findall(r'→ RUN:\s*(.+?)(?:\n|$)', text)
        for cmd in run_matches:
            actions.append({"type": "run", "target": cmd.strip()})
        return actions

    async def chat_stream(self, user_input, on_token=None, on_action=None, on_done=None):
        if not self.provider.api_key:
            if on_token:
                on_token("[#f87171]API key not configured. Run: python setup_api.py[/]")
            if on_done:
                on_done()
            return

        if not self.conversation_active:
            self.messages = []
            self.conversation_active = True

        self.messages.append({"role": "user", "content": user_input})
        full_response = ""

        if on_token:
            on_token("[#a78bfa]◆ [/]", "stream")

        for ok, chunk in self.provider.stream_chat(self.messages, self._build_system_prompt()):
            if ok:
                full_response += chunk
                if on_token:
                    on_token(chunk, "stream")

        self.messages.append({"role": "assistant", "content": full_response})

        actions = self._parse_actions(full_response)
        for action in actions:
            if action["type"] == "create":
                if on_action:
                    on_action("create", action["target"])
                content = self._extract_content_for_path(full_response, action["target"])
                if content:
                    fp = Path(action["target"])
                    fp.parent.mkdir(parents=True, exist_ok=True)
                    fp.write_text(content)
                    if on_action:
                        on_action("created", str(fp))
            elif action["type"] == "run":
                if on_action:
                    on_action("run", action["target"])
                result = await self.executor.run_command(action["target"])
                if on_action:
                    if result["success"]:
                        out = result["stdout"].strip()[:300]
                        if out:
                            on_action("output", out)
                        on_action("done", "✓ Command completed")
                    else:
                        err = result["stderr"].strip()[:300]
                        if err:
                            on_action("error", err)

        store.remember(f"agent_conv_{user_input[:20]}", {"input": user_input, "response": full_response[:200]}, category="agent_chat")

        if on_done:
            on_done(full_response)

    def _extract_content_for_path(self, response, path):
        fname = os.path.basename(path)
        blocks = re.findall(r'```(\w+)?\n(.*?)```', response, re.DOTALL)
        best = ""
        for lang, content in blocks:
            content = content.strip()
            block_start = response.find(f"```{lang}\n{content}```")
            create_line = response.find(f"→ CREATE: {path}")
            if create_line >= 0 and abs(block_start - create_line) < 500:
                if len(content) > len(best):
                    best = content
        if not best:
            for lang, content in blocks:
                if fname in response[max(0, response.find(content) - 100):response.find(content)]:
                    if len(content) > len(best):
                        best = content
        return best

    async def debug_error(self, error_text, command="", on_analysis=None, on_fix=None):
        if not error_text:
            return
        debug_prompt = f"""Analyze this error:
Command: {command}
Error: {error_text}
Return:
ANALYSIS: <one line>
FIX: <exact fix command>"""
        ok, response = self.provider.chat([{"role": "user", "content": debug_prompt}], "Expert debugger.")
        if ok:
            analysis, fix = "", ""
            for line in response.split("\n"):
                if line.startswith("ANALYSIS:"):
                    analysis = line[9:].strip()
                elif line.startswith("FIX:"):
                    fix = line[4:].strip()
            if on_analysis and analysis:
                on_analysis(analysis)
            if on_fix and fix:
                on_fix(fix)
