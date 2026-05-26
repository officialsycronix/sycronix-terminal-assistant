import random, json, sys, os
from pathlib import Path
if __name__ != "__main__":
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from datetime import datetime
from sycronix.core.config import SYCRONIX_DIR, PROGRESS_FILE, LEADERBOARD_FILE
from sycronix.ui.theme import color, THEME, styled_panel
from sycronix.ui.banner import show_banner, CREDIT
from sycronix.tutor.questions import get_questions

QUIZ_SIZE = 10

prompt_style = Style([("prompt", "bold #a78bfa")])
psession = PromptSession()

GUIDE = (
    color.bold("\n  How to Use Linux Tutor\n")
    + color.muted("  " + "─" * 30 + "\n\n")
    + color.info("  l<num>  ") + color.muted("— ") + color.text("View lesson") + color.muted("         e.g. ") + color.primary("l1") + "\n"
    + color.info("  q<num>  ") + color.muted("— ") + color.text("Take quiz") + color.muted("          e.g. ") + color.primary("q1") + "\n"
    + color.info("  leaderboard") + color.muted(" — ") + color.text("Top scores") + "\n"
    + color.info("  /exit   ") + color.muted(" — ") + color.text("Leave tutor") + "\n\n"
    + color.muted("  ○ = not attempted    ") + color.success("✓ = completed")
)

LESSONS = [
    {"title": "File System Navigation", "content": """[bold #00d4ff]File System Navigation[/]

  [bold]pwd[/]  — Print working directory
  [bold]ls[/]   — List directory contents
  [bold]cd[/]   — Change directory
  [bold]find[/] — Search for files
  [bold]tree[/] — Show directory tree as a hierarchy

[bold #ff6b9d]Syntax & Examples:[/]

  $ [bold]pwd[/]
  /home/user

  $ [bold]ls -la[/]
  total 42
  drwxr-xr-x  5 user user  4096 Jan 1 12:00 .
  drwxr-xr-x  3 user user  4096 Jan 1 12:00 ..

  $ [bold]cd /var/log[/]
  $ [bold]find . -name "*.log"[/]
  ./syslog
  ./auth.log"""},
    {"title": "File Operations", "content": """[bold #00d4ff]File Operations[/]

  [bold]cp[/]    — Copy files/directories
  [bold]mv[/]    — Move/rename files
  [bold]rm[/]    — Remove files
  [bold]mkdir[/] — Create directories
  [bold]touch[/] — Create empty file
  [bold]cat[/]   — View file contents

[bold #ff6b9d]Syntax & Examples:[/]

  $ [bold]touch file.txt[/]          # Create empty file
  $ [bold]cp file.txt backup.txt[/]  # Copy file
  $ [bold]mv old.txt new.txt[/]      # Rename file
  $ [bold]mkdir myfolder[/]          # Create directory
  $ [bold]rm file.txt[/]             # Delete file
  $ [bold]rm -rf folder/[/]          # Delete folder (careful!)
  $ [bold]cat file.txt[/]            # View file content"""},
    {"title": "Permissions & Ownership", "content": """[bold #00d4ff]Permissions & Ownership[/]

  [bold]chmod[/]   — Change file permissions
  [bold]chown[/]   — Change file owner
  [bold]umask[/]   — Set default permissions
  [bold]ls -l[/]   — View permissions
  [bold]chmod +x[/] — Make executable

[bold #ff6b9d]Syntax & Examples:[/]

  $ [bold]ls -l script.sh[/]
  -rwxr-xr-x  1 user user  1024 Jan 1 12:00 script.sh

  $ [bold]chmod +x script.sh[/]       # Make executable
  $ [bold]chmod 755 folder[/]         # rwxr-xr-x
  $ [bold]chmod 600 secret.txt[/]     # rw-------
  $ [bold]chown root:root file[/]     # Change owner:group"""},
    {"title": "Process Management",
        "content": """[bold #00d4ff]Process Management[/]

  [bold]ps[/]     — List running processes
  [bold]top[/]    — Live process viewer
  [bold]kill[/]   — Terminate process
  [bold]bg[/]     — Background a job
  [bold]fg[/]     — Foreground a job
  [bold]nohup[/]  — Run immune to hangups

[bold #ff6b9d]Syntax & Examples:[/]

  $ [bold]ps aux[/]                   # All processes
  $ [bold]top[/]                      # Live monitor (q to quit)
  $ [bold]kill -9 1234[/]             # Force kill PID 1234
  $ [bold]kill -15 1234[/]            # Graceful kill
  $ [bold]nohup python bot.py &[/]    # Run in background"""},
    {"title": "Text Processing",
        "content": """[bold #00d4ff]Text Processing Tools[/]

  [bold]grep[/]  — Search text for patterns
  [bold]sed[/]   — Stream editor (find & replace)
  [bold]awk[/]   — Text processing & reporting
  [bold]sort[/]  — Sort lines alphabetically
  [bold]wc[/]    — Word / line / char count
  [bold]cut[/]   — Extract columns from text

[bold #ff6b9d]Syntax & Examples:[/]

  $ [bold]grep "error" /var/log/syslog[/]
  Jan 1 12:00:01 host kernel: [123] error

  $ [bold]cat file.txt | wc -l[/]      # Line count
  $ [bold]sort names.txt[/]            # Sort alphabetically
  $ [bold]sed 's/old/new/g' file[/]    # Replace text
  $ [bold]cut -d: -f1 /etc/passwd[/]   # First column"""},
    {"title": "Package Management",
        "content": """[bold #00d4ff]Package Management (APT)[/]

  [bold]apt[/]      — Advanced Package Tool
  [bold]apt-get[/]  — Older package manager
  [bold]dpkg[/]     — Debian package manager
  [bold]pkg[/]      — Termux package manager

[bold #ff6b9d]Syntax & Examples:[/]

  $ [bold]pkg update && pkg upgrade[/]     # Update all
  $ [bold]pkg install python[/]            # Install package
  $ [bold]pkg search python[/]             # Search packages
  $ [bold]pkg uninstall python[/]          # Remove package
  $ [bold]apt list --installed[/]          # List installed"""},
    {"title": "User Management",
        "content": """[bold #00d4ff]User & Group Management[/]

  [bold]whoami[/]  — Current username
  [bold]who[/]     — Who is logged in
  [bold]id[/]      — User & group IDs
  [bold]useradd[/] — Add new user
  [bold]passwd[/]  — Change password
  [bold]su[/]      — Switch user
  [bold]sudo[/]    — Superuser do

[bold #ff6b9d]Syntax & Examples:[/]

  $ [bold]whoami[/]
  root

  $ [bold]id[/]
  uid=0(root) gid=0(root) groups=0(root)

  $ [bold]useradd -m john[/]          # Add user with home
  $ [bold]passwd john[/]              # Set password
  $ [bold]su - john[/]                # Switch to john
  $ [bold]sudo apt update[/]          # Run as root"""},
    {"title": "Archiving & Compression",
        "content": """[bold #00d4ff]Archiving & Compression[/]

  [bold]tar[/]     — Archive files
  [bold]gzip[/]    — Compress files
  [bold]gunzip[/]  — Decompress .gz files
  [bold]zip[/]     — Zip compression
  [bold]unzip[/]   — Extract .zip files

[bold #ff6b9d]Syntax & Examples:[/]

  $ [bold]tar -cvf archive.tar folder/[/]      # Create tar
  $ [bold]tar -xvf archive.tar[/]              # Extract tar
  $ [bold]tar -czvf archive.tar.gz folder/[/]  # Tar + gzip
  $ [bold]tar -xzvf archive.tar.gz[/]          # Extract .tar.gz
  $ [bold]zip -r archive.zip folder/[/]        # Create zip
  $ [bold]unzip archive.zip[/]                 # Extract zip"""},
    {"title": "Networking",
        "content": """[bold #00d4ff]Networking Commands[/]

  [bold]ping[/]     — Test network connectivity
  [bold]curl[/]     — Transfer data from URLs
  [bold]wget[/]     — Download files
  [bold]netstat[/]  — Network statistics
  [bold]ip[/]       — Network interface config
  [bold]nslookup[/] — DNS lookup

[bold #ff6b9d]Syntax & Examples:[/]

  $ [bold]ping -c 4 google.com[/]            # Ping 4 times
  $ [bold]curl ifconfig.me[/]                # Show public IP
  $ [bold]curl -O https://example.com/file[/] # Download file
  $ [bold]wget https://example.com/file[/]    # Download file
  $ [bold]ip addr[/]                          # Show IP addresses
  $ [bold]netstat -tulpn[/]                   # Listening ports"""},
    {"title": "SSH & Remote Access",
        "content": """[bold #00d4ff]SSH & Remote Access[/]

  [bold]ssh[/]       — Secure Shell (remote login)
  [bold]scp[/]       — Secure copy over SSH
  [bold]rsync[/]     — Sync files remotely
  [bold]ssh-keygen[/] — Generate SSH keys
  [bold]ssh-copy-id[/] — Copy SSH key to server

[bold #ff6b9d]Syntax & Examples:[/]

  $ [bold]ssh user@192.168.1.100[/]         # Remote login
  $ [bold]ssh -p 2222 user@host[/]          # Custom port
  $ [bold]scp file.txt user@host:/tmp/[/]   # Copy file to remote
  $ [bold]scp user@host:/remote/file .[/]   # Copy from remote
  $ [bold]rsync -avz folder/ user@host:~/  # Sync folder
  $ [bold]ssh-keygen -t rsa -b 4096[/]     # Generate key pair"""},
]

def run_tutor():
    console = Console()
    progress = _load_progress()

    console.print()
    show_banner()
    console.print(styled_panel(
        color.primary("Linux Mastery Tutor")
        + color.muted("\nLearn Linux commands with interactive lessons, examples, and quizzes.")
        + GUIDE,
        "Welcome"
    ))
    console.print()

    while True:
        console.print(color.heading("── Lessons ──"))
        for i, lesson in enumerate(LESSONS, 1):
            completed = progress.get(str(i), {}).get("completed", False)
            status = color.success("✓") if completed else color.muted("○")
            score = progress.get(str(i), {}).get("best", 0)
            console.print(f"  {status} {i}. {lesson['title']}  {color.muted(f'[{score}/{QUIZ_SIZE}]')}")

        console.print()
        console.print(color.muted("  l<num> - view lesson    q<num> - take quiz"))
        console.print(color.muted("  leaderboard - top scores    /exit - quit"))
        console.print()

        try:
            choice = psession.prompt("tutor> ", style=prompt_style).strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not choice:
            continue
        if choice == "/exit":
            break
        if choice == "leaderboard":
            _show_leaderboard(console)
            continue

        if choice.startswith("l") and choice[1:].isdigit():
            idx = int(choice[1:]) - 1
            if 0 <= idx < len(LESSONS):
                lesson = LESSONS[idx]
                console.print(styled_panel(lesson["content"], lesson["title"]))
                continue

        if choice.startswith("q") and choice[1:].isdigit():
            idx = int(choice[1:]) - 1
            if 0 <= idx < len(LESSONS):
                _take_quiz(console, idx, LESSONS[idx], progress)
                _save_progress(progress)
                continue

        console.print(color.error("Invalid choice. Try l1, q1, leaderboard, or /exit"))

    console.print(styled_panel(color.muted("Keep learning with ") + color.primary("SYCRONIX BOT") + color.muted("!"), "Goodbye"))

def _take_quiz(console, idx, lesson, progress):
    questions = get_questions(idx, QUIZ_SIZE)
    if not questions:
        console.print(color.error("No questions available for this lesson."))
        return

    score = 0
    wrong = []

    console.print()
    console.print(styled_panel(
        color.bold(lesson["title"]) + color.muted(f"  ({QUIZ_SIZE} questions)"),
        "Quiz"
    ))

    for q in questions:
        opts = q["opts"][:]
        random.shuffle(opts)
        console.print(color.bold(f"\n  {q['q']}"))
        for i, opt in enumerate(opts, 1):
            console.print(f"    {i}. {opt}")

        try:
            ans = psession.prompt("  Answer (1-4): ", style=prompt_style).strip()
        except (KeyboardInterrupt, EOFError):
            break

        if ans.isdigit():
            idx_a = int(ans) - 1
            if 0 <= idx_a < len(opts):
                if opts[idx_a] == q["a"]:
                    score += 1
                    console.print(color.success("  ✓ Correct!"))
                else:
                    console.print(color.error(f"  ✗ Incorrect. Answer: {q['a']}"))
                    wrong.append(q)
                continue
        console.print(color.error(f"  ✗ Incorrect. Answer: {q['a']}"))
        wrong.append(q)

    console.print()
    progress[str(idx + 1)] = {
        "completed": score == QUIZ_SIZE,
        "score": score,
        "best": max(progress.get(str(idx + 1), {}).get("best", 0), score),
        "total": QUIZ_SIZE,
    }

    if score == QUIZ_SIZE:
        console.print(styled_panel(color.success(f"Perfect score! {score}/{QUIZ_SIZE} 🎉"), "Result"))
    else:
        msg = color.warning(f"Score: {score}/{QUIZ_SIZE}")
        if wrong:
            msg += color.muted("\n\nReview wrong answers:")
            for w in wrong:
                msg += color.muted(f"\n  • {w['q']}")
                msg += color.success(f"\n    → {w['a']}")
        console.print(styled_panel(msg, "Result"))
    console.print()

def _show_leaderboard(console):
    lb = _load_leaderboard()
    if not lb:
        console.print(color.muted("No scores yet. Complete a quiz to appear!"))
        return

    sorted_lb = sorted(lb.items(), key=lambda x: x[1].get("score", 0), reverse=True)[:10]
    table = Table(box=box.ROUNDED, border_style=THEME["border"])
    table.add_column("Rank", style=THEME["primary"])
    table.add_column("Name", style=THEME["text"])
    table.add_column("Score", style=THEME["success"])
    table.add_column("Lessons", style=THEME["muted"])

    for rank, (name, data) in enumerate(sorted_lb, 1):
        table.add_row(str(rank), name, str(data.get("score", 0)), str(data.get("lessons", 0)))

    console.print(styled_panel(table, "Leaderboard"))
    console.print()

def _load_progress():
    try:
        if PROGRESS_FILE.exists():
            with open(PROGRESS_FILE) as f:
                return json.load(f)
    except:
        pass
    return {}

def _save_progress(progress):
    try:
        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress, f, indent=2)
    except:
        pass

def _load_leaderboard():
    try:
        if LEADERBOARD_FILE.exists():
            with open(LEADERBOARD_FILE) as f:
                return json.load(f)
    except:
        pass
    return {}
