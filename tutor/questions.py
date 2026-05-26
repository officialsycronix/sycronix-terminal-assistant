import random, sys, os
if __name__ != "__main__":
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)

Q_PER_LESSON = 200
QUIZ_SIZE = 10

def _make_q(text, answer, wrong_pool, exclude=None):
    exclude = exclude or []
    pool = [w for w in wrong_pool if w != answer and w not in exclude]
    if len(pool) < 3:
        pool = pool + ["unknown", "invalid", "none"]
    opts = [answer] + random.sample(pool, 3)
    random.shuffle(opts)
    return {"q": text, "a": answer, "opts": opts}

def _nav_questions():
    q = []
    cmds = [
        ("pwd", "print working directory", "shows current directory"),
        ("ls", "list directory contents", "lists files/folders"),
        ("cd", "change directory", "navigate to another folder"),
        ("find", "search for files by name", "finds files matching a pattern"),
        ("tree", "show directory as tree", "displays folder hierarchy"),
        ("mkdir", "create directories", "makes new folders"),
        ("rmdir", "remove empty directories", "deletes empty folders"),
        ("locate", "fast file search via database", "finds files quickly"),
        ("which", "locate a command's path", "shows executable location"),
        ("du", "estimate disk usage", "shows file/dir size"),
        ("df", "report free disk space", "shows available storage"),
        ("readlink", "resolve symbolic link", "shows symlink target"),
        ("realpath", "canonicalize path", "shows absolute path"),
        ("pushd", "push directory to stack", "saves and changes dir"),
        ("popd", "pop directory from stack", "restores saved dir"),
        ("dirs", "display directory stack", "shows saved directories"),
        ("file", "determine file type", "identifies file format"),
        ("stat", "display file status", "shows file metadata"),
        ("basename", "strip directory from path", "extracts filename"),
        ("dirname", "strip filename from path", "extracts directory path"),
        ("ln", "create hard/symbolic links", "creates file links"),
        ("readlink", "print symlink target", "shows where link points"),
        ("chattr", "change file attributes", "sets ext4 attributes"),
        ("lsattr", "list file attributes", "shows ext4 attributes"),
    ]
    all_cmds = [c[0] for c in cmds]
    for cmd, desc, explain in cmds:
        q.append(_make_q(f"What does '{cmd}' do?", desc, [e[1] for e in cmds if e[0] != cmd]))
        q.append(_make_q(f"Which command {explain}?", cmd, all_cmds))
        q.append(_make_q(f"What is '{cmd}' used for?", explain.capitalize() + ".", [e[2].capitalize() + "." for e in cmds if e[0] != cmd]))
    q.append(_make_q("Which command shows your current location?", "pwd", all_cmds))
    q.append(_make_q("Which command lists files and directories?", "ls", all_cmds))
    q.append(_make_q("Which command changes the current directory?", "cd", all_cmds))
    q.append(_make_q("How do you create a new directory?", "mkdir", all_cmds))
    q.append(_make_q("Which command searches for files?", "find", all_cmds))
    q.append(_make_q("What does 'pwd' stand for?", "Print Working Directory", ["Process Working Data", "Path With Data", "Program Word Display"]))
    q.append(_make_q("Which command shows disk space usage?", "df", all_cmds))
    q.append(_make_q("Which command shows file/directory sizes?", "du", all_cmds))
    q.append(_make_q("Which command resolves symbolic links?", "readlink", all_cmds))
    q.append(_make_q("What does 'realpath' do?", "Shows the absolute path of a file", ["Creates a real path", "Copies a real file", "Deletes a path"]))
    q.append(_make_q("How do you save and change directory?", "pushd", all_cmds))
    q.append(_make_q("How do you return to saved directory?", "popd", all_cmds))
    q.append(_make_q("Which command shows the directory stack?", "dirs", all_cmds))
    q.append(_make_q("What does 'file' command determine?", "The type of a file", ["File size", "File owner", "File permissions"]))
    q.append(_make_q("What does 'stat' display?", "File metadata and status", ["File contents", "File type only", "Directory listing"]))
    q.append(_make_q("Which command extracts filename from path?", "basename", all_cmds))
    q.append(_make_q("Which command extracts directory from path?", "dirname", all_cmds))
    q.append(_make_q("What flag with ls shows hidden files?", "-a", ["-l", "-h", "-r"]))
    q.append(_make_q("What flag with ls shows details?", "-l", ["-a", "-h", "-r"]))
    q.append(_make_q("What flag with du gives total size?", "-s", ["-h", "-a", "-c"]))
    q.append(_make_q("Which command is fastest for searching files?", "locate", all_cmds))
    q.append(_make_q("What must be updated for locate to find new files?", "The locate database", ["The kernel", "The filesystem", "Package manager"]))
    q.append(_make_q("What does 'cd -' do?", "Goes to previous directory", ["Goes home", "Shows path", "Clears screen"]))
    q.append(_make_q("What flag with ls shows sizes human-readable?", "-h", ["-a", "-l", "-r"]))
    q.append(_make_q("Which command creates symbolic links?", "ln -s", all_cmds))
    q.append(_make_q("Which command makes a file immutable?", "chattr +i", all_cmds))
    random.shuffle(q)
    return q[:Q_PER_LESSON]

def _file_questions():
    q = []
    cmds = [
        ("cp", "copy files", ["mv", "rm", "cat", "ln"]),
        ("mv", "move or rename", ["cp", "rm", "cat", "touch"]),
        ("rm", "remove files", ["cp", "mv", "cat", "touch"]),
        ("touch", "create empty file", ["cat", "echo", "mkdir", "cp"]),
        ("cat", "view file content", ["echo", "less", "head", "tail"]),
        ("less", "page through files", ["cat", "more", "head", "tail"]),
        ("more", "page through files (simpler)", ["less", "cat", "head", "tail"]),
        ("head", "show first lines", ["tail", "cat", "less", "more"]),
        ("tail", "show last lines", ["head", "cat", "less", "more"]),
        ("ln", "create file links", ["cp", "mv", "ls", "readlink"]),
        ("dd", "convert and copy data", ["cp", "cat", "mv", "tee"]),
        ("tee", "split output to file+screen", ["cat", "dd", "cp", "echo"]),
        ("install", "copy with attributes", ["cp", "mv", "chmod", "dd"]),
        ("truncate", "shrink/extend files", ["dd", "cp", "touch", "rm"]),
        ("shred", "securely delete files", ["rm", "dd", "wipe", "erase"]),
        ("sync", "flush filesystem buffers", ["fsync", "mount", "umount", "dd"]),
        ("mktemp", "create temp file safely", ["touch", "tempfile", "mkstemp", "cat"]),
        ("tac", "reverse file content", ["rev", "cat -r", "tail -r", "sort -r"]),
        ("diff", "compare files line by line", ["cmp", "comm", "patch", "sdiff"]),
        ("cmp", "compare files byte by byte", ["diff", "comm", "patch", "md5sum"]),
        ("comm", "compare sorted files", ["diff", "cmp", "join", "paste"]),
        ("patch", "apply diff to file", ["diff", "sed", "awk", "comm"]),
        ("sdiff", "side-by-side diff", ["diff", "cmp", "comm", "patch"]),
    ]
    all_cmds = [c[0] for c in cmds]
    for cmd, desc, _ in cmds:
        q.append(_make_q(f"What does '{cmd}' do?", desc, [e[1] for e in cmds if e[0] != cmd]))
        q.append(_make_q(f"Which command {desc}?", cmd, all_cmds))
    q.append(_make_q("Which command copies files?", "cp", all_cmds))
    q.append(_make_q("Which command moves or renames?", "mv", all_cmds))
    q.append(_make_q("Which command deletes files?", "rm", all_cmds))
    q.append(_make_q("How do you create an empty file?", "touch", all_cmds))
    q.append(_make_q("Which command views file content?", "cat", all_cmds))
    q.append(_make_q("What does 'cp -r' do?", "Copies directories recursively", ["Copies quickly", "Renames", "Removes", "Reads"]))
    q.append(_make_q("Which flag with rm removes directories?", "-rf", ["-r", "-f", "-d", "-i"]))
    q.append(_make_q("Which command pages through files?", "less", all_cmds))
    q.append(_make_q("Which command shows first 10 lines?", "head", all_cmds))
    q.append(_make_q("Which command shows last 10 lines?", "tail", all_cmds))
    q.append(_make_q("Which flag with tail follows file growth?", "-f", ["-F", "-n", "-r", "-c"]))
    q.append(_make_q("Which command creates links?", "ln", all_cmds))
    q.append(_make_q("Which flag with ln creates a symbolic link?", "-s", ["-h", "-l", "-f", "-p"]))
    q.append(_make_q("Which flag with cp preserves attributes?", "-p", ["-r", "-a", "-f", "-v"]))
    q.append(_make_q("What does 'cat -n' do?", "Shows line numbers", ["Shows non-printable", "Numbers pages", "Numbers words"]))
    q.append(_make_q("Which flag with head shows custom line count?", "-n", ["-c", "-l", "-f", "-v"]))
    q.append(_make_q("How do you view file in reverse order?", "tac", all_cmds))
    q.append(_make_q("Which command shows file differences?", "diff", all_cmds))
    q.append(_make_q("Which command compares files byte by byte?", "cmp", all_cmds))
    q.append(_make_q("Which command applies a diff patch?", "patch", all_cmds))
    q.append(_make_q("What does 'dd' primarily do?", "Low level data copying", ["Delete files", "Download data", "Display directories"]))
    q.append(_make_q("Which command splits output to file and terminal?", "tee", all_cmds))
    q.append(_make_q("Which command securely deletes files?", "shred", all_cmds))
    q.append(_make_q("Which command creates a temporary file safely?", "mktemp", all_cmds))
    q.append(_make_q("Which command flushes disk buffers?", "sync", all_cmds))
    random.shuffle(q)
    return q[:Q_PER_LESSON]

def _perm_questions():
    q = []
    modes = [
        ("777", "rwxrwxrwx", "All can do everything"),
        ("755", "rwxr-xr-x", "Owner full; others read/execute"),
        ("700", "rwx------", "Only owner can access"),
        ("644", "rw-r--r--", "Owner write; others read"),
        ("600", "rw-------", "Only owner read/write"),
        ("500", "r-x------", "Owner read/execute only"),
        ("400", "r--------", "Owner read only"),
        ("000", "---------", "No access for anyone"),
        ("555", "r-xr-xr-x", "All read/execute only"),
        ("711", "rwx--x--x", "Owner full; others execute"),
        ("666", "rw-rw-rw-", "All read/write"),
        ("111", "--x--x--x", "All execute only"),
        ("750", "rwxr-x---", "Owner full; group read/execute"),
        ("770", "rwxrwx---", "Owner and group full"),
        ("440", "r--r-----", "Owner and group read only"),
    ]
    syms = [s for _, s, _ in modes]
    perms = [p for p, _, _ in modes]
    for perm, sym, desc in modes:
        q.append(_make_q(f"What permission does octal {perm} represent?", sym, [s for s in syms if s != sym]))
        q.append(_make_q(f"Which octal permission is {sym}?", perm, [p for p in perms if p != perm]))
        q.append(_make_q(f"What does chmod {perm} mean?", desc, [d for _, _, d in modes if d != desc]))
    q.append(_make_q("Which permission is typical for scripts?", "755", perms))
    q.append(_make_q("Which permission is typical for config files?", "644", perms))
    q.append(_make_q("Which permission should SSH private keys have?", "600", perms))
    q.append(_make_q("What does chmod -R do?", "Changes permissions recursively", ["Removes all", "Resets to default", "Renames"]))
    q.append(_make_q("Which command changes file owner?", "chown", ["chmod", "umask", "chgrp", "chattr"]))
    q.append(_make_q("Which command changes group ownership?", "chgrp", ["chown", "chmod", "umask", "chattr"]))
    q.append(_make_q("Which command sets default permissions?", "umask", ["chmod", "chown", "chattr", "chgrp"]))
    q.append(_make_q("What umask gives default file 644?", "022", ["002", "077", "027", "007"]))
    q.append(_make_q("What umask gives default directory 755?", "022", ["002", "077", "027", "007"]))
    q.append(_make_q("What umask gives default file 600?", "077", ["022", "002", "027", "007"]))
    q.append(_make_q("What does SUID bit (u+s) do?", "Runs as file owner", ["Runs as group", "Runs as root", "Runs as user"]))
    q.append(_make_q("What does SGID bit (g+s) on a directory do?", "New files inherit group", ["Inherits owner", "Grants sudo", "Hides files"]))
    q.append(_make_q("What does sticky bit (+t) on /tmp do?", "Only owners can delete", ["Anyone can delete", "Files are hidden", "Files are encrypted"]))
    q.append(_make_q("What does 'ls -l' first column show?", "File type and permissions", ["File size", "File owner", "File name", "File date"]))
    q.append(_make_q("What does 'd' in 'drwxr-xr-x' mean?", "It is a directory", ["Device", "Symbolic link", "Regular file", "Socket"]))
    q.append(_make_q("What does 'l' in 'lrwxrwxrwx' mean?", "It is a symbolic link", ["Directory", "Regular file", "Socket", "Pipe"]))
    q.append(_make_q("What permission must a directory have to be accessible?", "Execute (x)", ["Read (r)", "Write (w)", "SUID (s)", "Sticky (t)"]))
    q.append(_make_q("Which command shows ACLs of a file?", "getfacl", ["setfacl", "ls -l", "stat", "chmod"]))
    q.append(_make_q("How to add group write permission?", "chmod g+w", ["chmod o+w", "chmod u+w", "chmod a+w", "chmod +w"]))
    q.append(_make_q("How to remove others' read permission?", "chmod o-r", ["chmod g-r", "chmod u-r", "chmod a-r", "chmod -r"]))
    q.append(_make_q("What does 'chmod a+x' do?", "Adds execute for everyone", ["Removes execute", "Adds write", "Adds read", "Sets SUID"]))
    q.append(_make_q("Which directory typically has sticky bit?", "/tmp", ["/etc", "/var", "/home", "/root"]))
    q.append(_make_q("What user categories exist in permissions?", "u, g, o, a", ["r, w, x", "1, 2, 3", "user, all", "owner, group"]))
    q.append(_make_q("Which command changes file attributes on ext4?", "chattr", ["chmod", "lsattr", "chown", "chgrp"]))
    q.append(_make_q("What does chattr +i do?", "Makes file immutable", ["Makes executable", "Makes hidden", "Makes read-only"]))
    random.shuffle(q)
    return q[:Q_PER_LESSON]

def _proc_questions():
    q = []
    cmds = [
        ("ps", "list running processes", ["top", "kill", "bg", "fg"]),
        ("top", "live process viewer", ["ps", "htop", "kill", "nice"]),
        ("kill", "terminate a process", ["ps", "top", "nice", "renice"]),
        ("bg", "background a job", ["fg", "jobs", "kill", "nohup"]),
        ("fg", "foreground a job", ["bg", "jobs", "kill", "nohup"]),
        ("jobs", "list background jobs", ["ps", "fg", "bg", "kill"]),
        ("nohup", "immune to hangups", ["disown", "bg", "fg", "kill"]),
        ("nice", "set priority", ["renice", "kill", "ps", "top"]),
        ("renice", "change priority", ["nice", "kill", "ps", "top"]),
        ("pgrep", "search processes by name", ["ps", "pkill", "kill", "top"]),
        ("pkill", "kill processes by name", ["pgrep", "kill", "killall", "ps"]),
        ("killall", "kill all by name", ["pkill", "kill", "pgrep", "ps"]),
        ("wait", "wait for processes", ["sleep", "bg", "fg", "jobs"]),
        ("sleep", "delay execution", ["wait", "timeout", "nohup", "bg"]),
        ("timeout", "run with time limit", ["sleep", "wait", "kill", "nohup"]),
        ("watch", "run command periodically", ["top", "ps", "sleep", "cron"]),
        ("uptime", "show system uptime", ["top", "w", "who", "last"]),
        ("pstree", "show process tree", ["ps", "top", "htop", "tree"]),
        ("strace", "trace system calls", ["ltrace", "perf", "gdb", "top"]),
        ("htop", "interactive process viewer", ["top", "ps", "kill", "vmstat"]),
    ]
    all_cmds = [c[0] for c in cmds]
    for cmd, desc, _ in cmds:
        q.append(_make_q(f"What does '{cmd}' do?", desc, [e[1] for e in cmds if e[0] != cmd]))
        q.append(_make_q(f"Which command {desc.lower()}?", cmd, all_cmds))
    q.append(_make_q("Which command lists running processes?", "ps", all_cmds))
    q.append(_make_q("Which command shows live processes?", "top", all_cmds))
    q.append(_make_q("Which command terminates a process?", "kill", all_cmds))
    q.append(_make_q("What does kill -9 do?", "Force kills the process", ["Pauses", "Resumes", "Restarts", "Stops gracefully"]))
    q.append(_make_q("What does kill -15 do?", "Gracefully terminates", ["Force kills", "Pauses", "Resumes", "Restarts"]))
    q.append(_make_q("Which command backgrounds a job?", "bg", all_cmds))
    q.append(_make_q("Which command brings job to foreground?", "fg", all_cmds))
    q.append(_make_q("Which command lists background jobs?", "jobs", all_cmds))
    q.append(_make_q("Which command ignores hangup signal?", "nohup", all_cmds))
    q.append(_make_q("Where does nohup save output by default?", "nohup.out", ["stdout", "output.log", "terminal", "/dev/null"]))
    q.append(_make_q("Which command sets process priority?", "nice", all_cmds))
    q.append(_make_q("Which command changes priority of running process?", "renice", all_cmds))
    q.append(_make_q("What is the nice value range?", "-20 to 19", ["0 to 100", "1 to 10", "-100 to 100", "0 to 39"]))
    q.append(_make_q("Which nice value is highest priority?", "-20", ["19", "0", "100", "-100"]))
    q.append(_make_q("What does 'ps aux' show?", "All processes from all users", ["Current user only", "Kernel threads", "System processes", "Background jobs"]))
    q.append(_make_q("What is PID 1 called?", "init/systemd", ["kernel", "shell", "root", "bios"]))
    q.append(_make_q("Which command searches processes by name?", "pgrep", all_cmds))
    q.append(_make_q("Which command kills processes by name?", "pkill", all_cmds))
    q.append(_make_q("Which command repeats a command periodically?", "watch", all_cmds))
    q.append(_make_q("What signal does Ctrl+C send?", "SIGINT", ["SIGTERM", "SIGKILL", "SIGSTOP", "SIGHUP"]))
    q.append(_make_q("What signal does Ctrl+Z send?", "SIGTSTP", ["SIGINT", "SIGTERM", "SIGKILL", "SIGSTOP"]))
    q.append(_make_q("What does '&' at end of command do?", "Runs in background", ["Runs as root", "Runs in foreground", "Runs silently", "Runs as daemon"]))
    q.append(_make_q("Which command shows system load average?", "uptime", all_cmds))
    q.append(_make_q("Which command shows process tree?", "pstree", all_cmds))
    q.append(_make_q("Which command traces system calls?", "strace", all_cmds))
    random.shuffle(q)
    return q[:Q_PER_LESSON]

def _text_questions():
    q = []
    cmds = [
        ("grep", "search text for patterns", ["sed", "awk", "cut", "sort"]),
        ("sed", "stream editor", ["grep", "awk", "cut", "tr"]),
        ("awk", "pattern scanning/processing", ["sed", "grep", "cut", "sort"]),
        ("sort", "sort lines of text", ["uniq", "wc", "cut", "awk"]),
        ("uniq", "remove duplicate lines", ["sort", "wc", "cut", "awk"]),
        ("wc", "word/line/char count", ["cat", "sort", "uniq", "cut"]),
        ("cut", "extract columns from text", ["awk", "sed", "sort", "uniq"]),
        ("tr", "translate or delete chars", ["sed", "awk", "cut", "sort"]),
        ("tee", "split output to file+stdout", ["cat", "dd", "cp", "echo"]),
        ("paste", "merge lines side by side", ["join", "cut", "awk", "sed"]),
        ("join", "join lines on common field", ["paste", "cut", "awk", "sed"]),
        ("comm", "compare two sorted files", ["diff", "cmp", "join", "paste"]),
        ("diff", "show file differences", ["comm", "cmp", "patch", "sdiff"]),
        ("patch", "apply diff changes", ["diff", "sed", "awk", "comm"]),
        ("fmt", "reformat paragraphs", ["fold", "pr", "cat", "sed"]),
        ("fold", "wrap long lines", ["fmt", "pr", "cat", "sed"]),
        ("pr", "paginate text for printing", ["fmt", "fold", "cat", "nl"]),
        ("nl", "number lines", ["cat -n", "pr", "fmt", "sort"]),
        ("od", "octal dump of file", ["hexdump", "xxd", "cat", "strings"]),
        ("strings", "extract strings from binary", ["od", "hexdump", "cat", "file"]),
        ("rev", "reverse each line", ["tac", "sort -r", "awk", "sed"]),
        ("expand", "convert tabs to spaces", ["unexpand", "tr", "sed", "awk"]),
        ("unexpand", "convert spaces to tabs", ["expand", "tr", "sed", "awk"]),
    ]
    all_cmds = [c[0] for c in cmds]
    for cmd, desc, _ in cmds:
        q.append(_make_q(f"What does '{cmd}' do?", desc, [e[1] for e in cmds if e[0] != cmd]))
        q.append(_make_q(f"Which command {desc.lower()}?", cmd, all_cmds))
    q.append(_make_q("Which command searches text for patterns?", "grep", all_cmds))
    q.append(_make_q("Which command does find and replace?", "sed", all_cmds))
    q.append(_make_q("Which command counts words/lines?", "wc", all_cmds))
    q.append(_make_q("Which command sorts lines?", "sort", all_cmds))
    q.append(_make_q("Which command removes duplicates?", "uniq", all_cmds))
    q.append(_make_q("Which command extracts columns?", "cut", all_cmds))
    q.append(_make_q("Which command translates characters?", "tr", all_cmds))
    q.append(_make_q("What does grep -i do?", "Case insensitive search", ["Invert match", "Show numbers", "Recursive", "Count only"]))
    q.append(_make_q("What does grep -r do?", "Recursive search", ["Reverse match", "Raw output", "Regular expr", "Count only"]))
    q.append(_make_q("What does grep -v do?", "Invert match", ["Verbose", "Version", "Show numbers", "Count only"]))
    q.append(_make_q("What does grep -c do?", "Count matching lines", ["Count chars", "Copy matches", "Concatenate", "Count files"]))
    q.append(_make_q("What does grep -n do?", "Show line numbers", ["Show names", "Natural sort", "No output", "Number files"]))
    q.append(_make_q("Which flag with sort does reverse?", "-r", ["-R", "-n", "-u", "-f"]))
    q.append(_make_q("Which flag with sort does numeric?", "-n", ["-N", "-r", "-u", "-f"]))
    q.append(_make_q("What does wc -l count?", "Lines", ["Words", "Chars", "Bytes", "Files"]))
    q.append(_make_q("What does wc -w count?", "Words", ["Lines", "Chars", "Bytes", "Files"]))
    q.append(_make_q("What does cut -d: do?", "Sets delimiter to :", ["Deletes colons", "Disables delimiter", "Default delimiter", "Doubles delimiter"]))
    q.append(_make_q("What does cut -f1 do?", "Extracts first field", ["First file", "Formats output", "Filters lines", "First char"]))
    q.append(_make_q("Which flag with uniq counts occurrences?", "-c", ["-d", "-u", "-i", "-f"]))
    q.append(_make_q("What does 'tr a-z A-Z' do?", "Lowercase to uppercase", ["Uppercase to lowercase", "Removes letters", "Reverses text", "Sorts chars"]))
    q.append(_make_q("Which command merges lines side by side?", "paste", all_cmds))
    q.append(_make_q("Which command joins on common field?", "join", all_cmds))
    q.append(_make_q("Which command compares two sorted files?", "comm", all_cmds))
    q.append(_make_q("Which command shows differences line by line?", "diff", all_cmds))
    q.append(_make_q("What does 'sed s/old/new/g' do?", "Replace all occurrences", ["Replace first only", "Delete old", "Append new", "Insert before"]))
    q.append(_make_q("Which command numbers lines?", "nl", all_cmds))
    q.append(_make_q("Which command extracts strings from binaries?", "strings", all_cmds))
    q.append(_make_q("What does 'fmt' do?", "Reformats paragraphs", ["Wraps lines", "Pages text", "Numbers lines", "Sorts text"]))
    q.append(_make_q("What does 'fold' do?", "Wraps long lines at width", ["Reformats paragraphs", "Pages text", "Numbers lines", "Reverses text"]))
    q.append(_make_q("Which command reverses each line?", "rev", all_cmds))
    q.append(_make_q("Which command converts tabs to spaces?", "expand", all_cmds))
    random.shuffle(q)
    return q[:Q_PER_LESSON]

def _pkg_questions():
    q = []
    cmds = [
        ("pkg", "Termux package manager", ["apt", "dpkg", "pip", "brew"]),
        ("apt", "Debian package manager", ["dpkg", "snap", "pip", "brew"]),
        ("dpkg", "low-level Debian packager", ["apt", "snap", "pip", "brew"]),
        ("pip", "Python package installer", ["apt", "npm", "gem", "cargo"]),
        ("npm", "Node.js package manager", ["pip", "gem", "cargo", "apt"]),
        ("gem", "Ruby package manager", ["pip", "npm", "cargo", "apt"]),
        ("cargo", "Rust package manager", ["pip", "npm", "gem", "apt"]),
        ("brew", "Homebrew for macOS", ["apt", "snap", "pip", "npm"]),
        ("pacman", "Arch Linux package manager", ["apt", "yum", "dnf", "zypper"]),
        ("yum", "RHEL/CentOS 7 packager", ["dnf", "apt", "pacman", "zypper"]),
        ("dnf", "Fedora package manager", ["yum", "apt", "pacman", "zypper"]),
        ("zypper", "openSUSE package manager", ["apt", "yum", "dnf", "pacman"]),
        ("emerge", "Gentoo package manager", ["apt", "pacman", "yum", "dnf"]),
        ("snap", "Canonical snap packages", ["flatpak", "apt", "pip", "brew"]),
        ("flatpak", "cross-distro app format", ["snap", "apt", "pip", "brew"]),
        ("git", "version control system", ["apt", "pip", "npm", "cargo"]),
        ("make", "build from Makefile", ["cmake", "gcc", "apt", "pip"]),
        ("cmake", "cross-platform build system", ["make", "gcc", "apt", "pip"]),
        ("wget", "download files from URLs", ["curl", "apt", "pip", "git"]),
        ("curl", "transfer data with URLs", ["wget", "apt", "pip", "git"]),
    ]
    all_cmds = [c[0] for c in cmds]
    for cmd, desc, _ in cmds:
        q.append(_make_q(f"What does '{cmd}' do?", desc, [e[1] for e in cmds if e[0] != cmd]))
        q.append(_make_q(f"Which command {desc.lower()}?", cmd, all_cmds))
    q.append(_make_q("How to install packages on Termux?", "pkg install", all_cmds))
    q.append(_make_q("How to update all packages on Termux?", "pkg update && pkg upgrade", ["pkg upgrade all", "pkg refresh", "pkg update-all", "pkg sync"]))
    q.append(_make_q("How to search for a package on Termux?", "pkg search", all_cmds))
    q.append(_make_q("Which command installs Python packages?", "pip", all_cmds))
    q.append(_make_q("How to install a specific pip version?", "pip install package==version", ["pip install package@version", "pip install -v package", "pip add package", "pip get package"]))
    q.append(_make_q("Which command installs Node packages?", "npm", all_cmds))
    q.append(_make_q("Which command installs Ruby gems?", "gem", all_cmds))
    q.append(_make_q("Which command installs Rust crates?", "cargo", all_cmds))
    q.append(_make_q("What does 'apt update' do?", "Updates package index", ["Upgrades packages", "Installs updates", "Checks OS version", "Rebuilds cache"]))
    q.append(_make_q("What does 'apt upgrade' do?", "Upgrades all packages", ["Updates index", "Checks updates", "Upgrades system", "Installs kernel"]))
    q.append(_make_q("What does 'apt remove' do?", "Removes a package", ["Purges config", "Reinstalls", "Downgrades", "Updates"]))
    q.append(_make_q("What does 'apt purge' do?", "Removes package and config", ["Removes package only", "Purges cache", "Purges logs", "Reinstalls"]))
    q.append(_make_q("Which flag with dpkg installs a .deb?", "-i", ["-I", "-r", "-l", "-P"]))
    q.append(_make_q("Which flag with dpkg lists packages?", "-l", ["-L", "-I", "-s", "-p"]))
    q.append(_make_q("Which command downloads files?", "wget", all_cmds))
    q.append(_make_q("What does 'curl -O' do?", "Downloads with original name", ["Outputs to stdout", "Overwrites", "Opens browser", "Outputs JSON"]))
    q.append(_make_q("Which command clones repositories?", "git clone", all_cmds))
    q.append(_make_q("What does 'pip freeze' show?", "Installed packages with versions", ["Frozen packages", "Package cache", "Requirements file", "Pip config"]))
    q.append(_make_q("How to export pip packages?", "pip freeze > requirements.txt", ["pip export", "pip list > ", "pip save", "pip dump"]))
    q.append(_make_q("How to install from requirements.txt?", "pip install -r requirements.txt", ["pip install requirements.txt", "pip -r install", "pip read", "pip import"]))
    q.append(_make_q("Which package manager uses pacman?", "Arch Linux", ["Debian", "Fedora", "openSUSE", "Gentoo"]))
    q.append(_make_q("Which package manager uses dnf?", "Fedora", ["Debian", "Arch", "openSUSE", "Gentoo"]))
    q.append(_make_q("Which package manager uses emerge?", "Gentoo", ["Debian", "Fedora", "Arch", "openSUSE"]))
    q.append(_make_q("Which package manager uses zypper?", "openSUSE", ["Debian", "Fedora", "Arch", "Gentoo"]))
    q.append(_make_q("Which command builds from Makefile?", "make", all_cmds))
    q.append(_make_q("What does cmake generate?", "Build system files", ["Executables", "Source code", "Packages", "Documentation"]))
    q.append(_make_q("Which command installs snap packages?", "snap install", all_cmds))
    q.append(_make_q("Which command installs flatpak apps?", "flatpak install", all_cmds))
    random.shuffle(q)
    return q[:Q_PER_LESSON]

def _user_questions():
    q = []
    cmds = [
        ("whoami", "show current username", ["who", "id", "logname", "users"]),
        ("who", "show logged in users", ["w", "users", "whoami", "id"]),
        ("w", "show who is logged in and activity", ["who", "users", "uptime", "last"]),
        ("id", "show user/group IDs", ["whoami", "who", "groups", "logname"]),
        ("groups", "show user's groups", ["id", "whoami", "who", "members"]),
        ("useradd", "add a new user", ["usermod", "userdel", "passwd", "chage"]),
        ("usermod", "modify a user account", ["useradd", "userdel", "passwd", "chage"]),
        ("userdel", "delete a user account", ["useradd", "usermod", "passwd", "chage"]),
        ("passwd", "change user password", ["chpasswd", "gpasswd", "openssl", "shadow"]),
        ("su", "switch to another user", ["sudo", "login", "whoami", "bash"]),
        ("sudo", "execute as superuser", ["su", "doas", "pkexec", "runas"]),
        ("chage", "change password expiry", ["passwd", "usermod", "shadow", "age"]),
        ("gpasswd", "administer /etc/group", ["passwd", "chage", "groupmod", "grp"]),
        ("groupadd", "add a new group", ["groupdel", "groupmod", "addgroup", "grp"]),
        ("groupdel", "delete a group", ["groupadd", "groupmod", "delgroup", "grp"]),
        ("groupmod", "modify a group", ["groupadd", "groupdel", "gpasswd", "grp"]),
        ("last", "show last logins", ["who", "w", "history", "auth.log"]),
        ("lastlog", "last login for each user", ["last", "who", "w", "logins"]),
        ("faillog", "show failed logins", ["last", "who", "w", "auth.log"]),
        ("logname", "print original user", ["whoami", "who", "id", "users"]),
        ("newgrp", "log in to new group", ["sg", "groups", "id", "su"]),
        ("sg", "execute command as group", ["newgrp", "sudo", "su", "runas"]),
    ]
    all_cmds = [c[0] for c in cmds]
    for cmd, desc, _ in cmds:
        q.append(_make_q(f"What does '{cmd}' do?", desc, [e[1] for e in cmds if e[0] != cmd]))
        q.append(_make_q(f"Which command {desc.lower()}?", cmd, all_cmds))
    q.append(_make_q("Which command shows your username?", "whoami", all_cmds))
    q.append(_make_q("Which command shows logged in users?", "who", all_cmds))
    q.append(_make_q("Which command shows user and group IDs?", "id", all_cmds))
    q.append(_make_q("Which command adds a new user?", "useradd", all_cmds))
    q.append(_make_q("Which command modifies a user?", "usermod", all_cmds))
    q.append(_make_q("Which command deletes a user?", "userdel", all_cmds))
    q.append(_make_q("Which command changes password?", "passwd", all_cmds))
    q.append(_make_q("Which command switches user?", "su", all_cmds))
    q.append(_make_q("Which command executes as superuser?", "sudo", all_cmds))
    q.append(_make_q("Which file stores user account info?", "/etc/passwd", ["/etc/shadow", "/etc/group", "/etc/gshadow", "/etc/login"]))
    q.append(_make_q("Which file stores encrypted passwords?", "/etc/shadow", ["/etc/passwd", "/etc/group", "/etc/gshadow", "/etc/secure"]))
    q.append(_make_q("Which file stores group information?", "/etc/group", ["/etc/passwd", "/etc/shadow", "/etc/gshadow", "/etc/users"]))
    q.append(_make_q("What does 'sudo -i' do?", "Opens a root login shell", ["Installs package", "Shows help", "Lists users", "Shows config"]))
    q.append(_make_q("What does 'sudo -u' do?", "Runs as specified user", ["Updates user", "Upgrades system", "Shows users", "Unsets user"]))
    q.append(_make_q("What does 'su - username' do?", "Login shell switch", ["No env switch", "Updates user", "Shows info", "Unsets user"]))
    q.append(_make_q("Which command adds user to group?", "usermod -aG", all_cmds))
    q.append(_make_q("Which command creates a new group?", "groupadd", all_cmds))
    q.append(_make_q("Which command shows login history?", "last", all_cmds))
    q.append(_make_q("What is root's UID?", "0", ["1", "100", "65534", "1000"]))
    q.append(_make_q("What is nobody's UID typically?", "65534", ["0", "1", "100", "1000"]))
    q.append(_make_q("Which command sets password expiry?", "chage", all_cmds))
    q.append(_make_q("Which command edits sudoers safely?", "visudo", ["sudo vi", "vim /etc/sudoers", "nano /etc/sudoers", "emacs /etc/sudoers"]))
    q.append(_make_q("What does 'passwd -l' do?", "Locks the user account", ["Shows info", "Lists users", "Changes shell", "Unlocks user"]))
    q.append(_make_q("What does 'usermod -s' do?", "Changes login shell", ["Changes username", "Changes UID", "Changes home", "Changes group"]))
    q.append(_make_q("Which command shows failed logins?", "faillog", all_cmds))
    q.append(_make_q("Which command shows original user before su?", "logname", all_cmds))
    q.append(_make_q("Which command switches group?", "newgrp", all_cmds))
    random.shuffle(q)
    return q[:Q_PER_LESSON]

def _arch_questions():
    q = []
    cmds = [
        ("tar", "create/extract tape archives", ["gzip", "zip", "rar", "7z"]),
        ("gzip", "compress files (GNU zip)", ["tar", "bzip2", "xz", "zip"]),
        ("gunzip", "decompress .gz files", ["gzip", "bunzip2", "unxz", "unzip"]),
        ("bzip2", "high compression like gzip", ["gzip", "xz", "zip", "tar"]),
        ("bunzip2", "decompress .bz2 files", ["bzip2", "gunzip", "unxz", "unzip"]),
        ("xz", "very high compression", ["gzip", "bzip2", "zip", "lzma"]),
        ("unxz", "decompress .xz files", ["xz", "gunzip", "bunzip2", "unzip"]),
        ("zip", "cross-platform compression", ["tar", "gzip", "7z", "rar"]),
        ("unzip", "extract .zip files", ["zip", "tar", "7z", "rar"]),
        ("7z", "7-Zip high compression", ["zip", "tar", "gzip", "rar"]),
        ("rar", "RAR compression format", ["zip", "7z", "tar", "unrar"]),
        ("unrar", "extract .rar files", ["rar", "zip", "7z", "tar"]),
        ("lz4", "extremely fast compression", ["gzip", "bzip2", "xz", "zstd"]),
        ("zstd", "Zstandard compression", ["gzip", "bzip2", "xz", "lz4"]),
        ("unzstd", "decompress .zst files", ["zstd", "gzip", "bzip2", "xz"]),
        ("cpio", "copy files to/from archives", ["tar", "pax", "dd", "dump"]),
        ("pax", "portable archive interchange", ["tar", "cpio", "dd", "dump"]),
        ("ar", "create static library archives", ["tar", "cpio", "dd", "ld"]),
        ("lzop", "fast LZO compression", ["gzip", "bzip2", "xz", "lz4"]),
        ("brotli", "Brotli compression", ["gzip", "bzip2", "xz", "zstd"]),
    ]
    all_cmds = [c[0] for c in cmds]
    for cmd, desc, _ in cmds:
        q.append(_make_q(f"What does '{cmd}' do?", desc, [e[1] for e in cmds if e[0] != cmd]))
        q.append(_make_q(f"Which command {desc.lower()}?", cmd, all_cmds))
    q.append(_make_q("Which command creates tar archives?", "tar", all_cmds))
    q.append(_make_q("Which tar flag creates an archive?", "-cvf", ["-xvf", "-tvf", "-rvf", "-uvf"]))
    q.append(_make_q("Which tar flag extracts an archive?", "-xvf", ["-cvf", "-tvf", "-rvf", "-uvf"]))
    q.append(_make_q("Which tar flag adds gzip compression?", "-z", ["-j", "-J", "-Z", "-a"]))
    q.append(_make_q("Which tar flag adds bzip2 compression?", "-j", ["-z", "-J", "-Z", "-a"]))
    q.append(_make_q("Which tar flag adds xz compression?", "-J", ["-z", "-j", "-Z", "-a"]))
    q.append(_make_q("How to extract a tar.gz file?", "tar -xzvf", ["tar -xjvf", "tar -xvf", "gzip -d", "gunzip"]))
    q.append(_make_q("How to extract a tar.bz2 file?", "tar -xjvf", ["tar -xzvf", "tar -xvf", "bzip2 -d", "bunzip2"]))
    q.append(_make_q("How to compress a file with gzip?", "gzip file", ["gunzip file", "compress file", "zip file", "gzip -d file"]))
    q.append(_make_q("Which compression gives highest ratio?", "xz", ["gzip", "bzip2", "zip", "lz4"]))
    q.append(_make_q("Which compression is fastest?", "lz4", ["gzip", "bzip2", "xz", "zstd"]))
    q.append(_make_q("Which command creates zip files?", "zip", all_cmds))
    q.append(_make_q("Which zip flag adds recursively?", "-r", ["-R", "-z", "-f", "-d"]))
    q.append(_make_q("Which command extracts zip files?", "unzip", all_cmds))
    q.append(_make_q("Which command uses Zstandard?", "zstd", all_cmds))
    q.append(_make_q("Which tar flag lists contents?", "-tvf", ["-xvf", "-cvf", "-rvf", "-uvf"]))
    q.append(_make_q("Which tar flag appends to archive?", "-rvf", ["-cvf", "-xvf", "-tvf", "-uvf"]))
    q.append(_make_q("What does gzip -k do?", "Keeps original file", ["Kills process", "Key file", "Kraken mode", "Kernel mode"]))
    q.append(_make_q("What zip level gives max compression?", "9", ["0", "5", "1", "99"]))
    q.append(_make_q("What extension does bzip2 produce?", ".bz2", [".gz", ".xz", ".zst", ".lz4"]))
    q.append(_make_q("What extension does xz produce?", ".xz", [".gz", ".bz2", ".zst", ".lz4"]))
    q.append(_make_q("What flag with gzip sets compression level?", "-1 to -9", ["-0 to -9", "-f to -F", "-s to -S", "-a to -z"]))
    q.append(_make_q("Which command creates tar with xz?", "tar -cJvf", ["tar -czvf", "tar -cjvf", "tar -cZvf", "tar -cvf"]))
    q.append(_make_q("Which command copies files to archive?", "cpio", all_cmds))
    q.append(_make_q("Which command creates static library?", "ar", all_cmds))
    q.append(_make_q("Which command uses Brotli compression?", "brotli", all_cmds))
    random.shuffle(q)
    return q[:Q_PER_LESSON]

def _net_questions():
    q = []
    cmds = [
        ("ping", "test network connectivity", ["traceroute", "curl", "wget", "nc"]),
        ("traceroute", "trace network path", ["ping", "mtr", "path", "route"]),
        ("mtr", "combine ping and traceroute", ["traceroute", "ping", "netstat", "ip"]),
        ("curl", "transfer data with URLs", ["wget", "nc", "ftp", "ssh"]),
        ("wget", "download files from web", ["curl", "nc", "ftp", "ssh"]),
        ("nc", "netcat TCP/UDP Swiss army knife", ["nmap", "telnet", "ssh", "ftp"]),
        ("nmap", "network port scanner", ["nc", "ping", "traceroute", "dig"]),
        ("netstat", "network statistics", ["ss", "ip", "ifconfig", "route"]),
        ("ss", "socket statistics (modern)", ["netstat", "ip", "ifconfig", "route"]),
        ("ip", "show/manipulate routing", ["ifconfig", "route", "netstat", "ss"]),
        ("ifconfig", "configure network interface", ["ip", "iwconfig", "netstat", "route"]),
        ("iwconfig", "configure wireless interface", ["ifconfig", "ip", "nmcli", "iwlist"]),
        ("route", "show routing table", ["ip route", "netstat", "traceroute", "ping"]),
        ("dig", "DNS lookup tool", ["nslookup", "host", "whois", "curl"]),
        ("nslookup", "query DNS servers", ["dig", "host", "whois", "curl"]),
        ("host", "simple DNS lookup", ["dig", "nslookup", "whois", "curl"]),
        ("whois", "domain registration lookup", ["dig", "nslookup", "host", "curl"]),
        ("ssh", "secure shell remote login", ["telnet", "scp", "rsync", "sftp"]),
        ("scp", "secure copy over SSH", ["rsync", "sftp", "ssh", "cp"]),
        ("rsync", "remote file sync", ["scp", "sftp", "ssh", "cp"]),
        ("sftp", "secure file transfer", ["scp", "rsync", "ssh", "ftp"]),
        ("ftp", "file transfer protocol", ["sftp", "scp", "rsync", "curl"]),
        ("telnet", "unencrypted remote terminal", ["ssh", "nc", "rlogin", "tn"]),
        ("iperf", "network bandwidth test", ["ping", "speedtest", "nc", "nmap"]),
        ("nmcli", "NetworkManager CLI", ["iwconfig", "ifconfig", "ip", "netplan"]),
    ]
    all_cmds = [c[0] for c in cmds]
    for cmd, desc, _ in cmds:
        q.append(_make_q(f"What does '{cmd}' do?", desc, [e[1] for e in cmds if e[0] != cmd]))
        q.append(_make_q(f"Which command {desc.lower()}?", cmd, all_cmds))
    q.append(_make_q("Which command tests connectivity?", "ping", all_cmds))
    q.append(_make_q("Which command traces network path?", "traceroute", all_cmds))
    q.append(_make_q("Which command downloads files?", "wget", all_cmds))
    q.append(_make_q("What does 'curl ifconfig.me' show?", "Your public IP", ["Local IP", "DNS config", "Network speed", "Gateway IP"]))
    q.append(_make_q("What does ping -c 4 do?", "Sends 4 packets", ["Continuous ping", "Check port 4", "IPv4 only", "Count hosts"]))
    q.append(_make_q("Which command scans ports?", "nmap", all_cmds))
    q.append(_make_q("Which command shows listening ports?", "netstat -tulpn", all_cmds))
    q.append(_make_q("Which command shows socket statistics?", "ss", all_cmds))
    q.append(_make_q("What does 'ip addr' show?", "IP addresses", ["Adds IP", "Shows ARP", "Shows routing", "Shows links"]))
    q.append(_make_q("Which command shows routing table?", "ip route", all_cmds))
    q.append(_make_q("Which command does DNS lookup?", "dig", all_cmds))
    q.append(_make_q("Which command does reverse DNS lookup?", "dig -x", all_cmds))
    q.append(_make_q("Which command shows domain info?", "whois", all_cmds))
    q.append(_make_q("Which command connects via SSH?", "ssh", all_cmds))
    q.append(_make_q("Which port does SSH use?", "22", ["21", "80", "443", "2222"]))
    q.append(_make_q("Which port does HTTP use?", "80", ["443", "22", "21", "8080"]))
    q.append(_make_q("Which port does HTTPS use?", "443", ["80", "22", "21", "8080"]))
    q.append(_make_q("Which port does FTP use?", "21", ["22", "80", "443", "23"]))
    q.append(_make_q("What does 'ping 127.0.0.1' test?", "Local network stack", ["Internet", "DNS", "Gateway", "Router"]))
    q.append(_make_q("Which command securely copies files?", "scp", all_cmds))
    q.append(_make_q("Which command syncs files efficiently?", "rsync", all_cmds))
    q.append(_make_q("What flag with wget continues download?", "-c", ["-r", "-m", "-b", "-q"]))
    q.append(_make_q("Which command is netcat?", "nc", all_cmds))
    q.append(_make_q("Which command tests bandwidth?", "iperf", all_cmds))
    q.append(_make_q("Which command manages NetworkManager?", "nmcli", all_cmds))
    q.append(_make_q("Which command shows ARP cache?", "ip neigh", all_cmds))
    q.append(_make_q("Which command configures wireless?", "iwconfig", all_cmds))
    random.shuffle(q)
    return q[:Q_PER_LESSON]

def _ssh_questions():
    q = []
    cmds = [
        ("ssh", "secure shell remote login", ["telnet", "scp", "rsync", "sftp"]),
        ("ssh-keygen", "generate SSH key pairs", ["ssh-add", "ssh-copy-id", "openssl", "gpg"]),
        ("ssh-copy-id", "copy key to remote server", ["ssh-keygen", "ssh-add", "scp", "rsync"]),
        ("ssh-add", "add key to SSH agent", ["ssh-keygen", "ssh-copy-id", "ssh-agent", "keychain"]),
        ("ssh-agent", "manage SSH keys in memory", ["ssh-add", "keychain", "gpg-agent", "ssh"]),
        ("ssh-keyscan", "scan remote host keys", ["nmap", "ssh", "dig", "nc"]),
        ("sftp", "secure file transfer protocol", ["scp", "rsync", "ssh", "ftp"]),
        ("scp", "secure copy over SSH", ["rsync", "sftp", "ssh", "cp"]),
        ("rsync", "efficient remote sync", ["scp", "sftp", "ssh", "cp"]),
        ("autossh", "auto-reconnecting SSH tunnel", ["ssh", "mosh", "telnet", "nc"]),
        ("mosh", "mobile shell (roaming)", ["ssh", "telnet", "autossh", "nc"]),
        ("sshfs", "mount remote via SSH", ["sftp", "scp", "nfs", "cifs"]),
        ("sshd", "SSH daemon (server)", ["ssh", "ssh-keygen", "ssh-agent", "ssh-add"]),
    ]
    all_cmds = [c[0] for c in cmds]
    for cmd, desc, _ in cmds:
        q.append(_make_q(f"What does '{cmd}' do?", desc, [e[1] for e in cmds if e[0] != cmd]))
        q.append(_make_q(f"Which command {desc.lower()}?", cmd, all_cmds))
    q.append(_make_q("Which command connects via SSH?", "ssh", all_cmds))
    q.append(_make_q("How to connect to SSH on port 2222?", "ssh -p 2222 user@host", ["ssh user@host:2222", "ssh 2222 user@host", "ssh user@host -P 2222", "ssh -P 2222 user@host"]))
    q.append(_make_q("Which command generates SSH keys?", "ssh-keygen", all_cmds))
    q.append(_make_q("Which command copies SSH keys to server?", "ssh-copy-id", all_cmds))
    q.append(_make_q("Which command adds key to agent?", "ssh-add", all_cmds))
    q.append(_make_q("Which command starts SSH agent?", "ssh-agent", all_cmds))
    q.append(_make_q("Which algorithm is best for SSH keys?", "Ed25519", ["RSA", "DSA", "ECDSA", "Diffie-Hellman"]))
    q.append(_make_q("Where are user SSH keys stored?", "~/.ssh/", ["/etc/ssh/", "~/.config/ssh/", "/root/ssh/", "~/.ssh_keys/"]))
    q.append(_make_q("Which file is the private SSH key?", "id_rsa", ["id_rsa.pub", "authorized_keys", "known_hosts", "config"]))
    q.append(_make_q("Which file is the public SSH key?", "id_rsa.pub", ["id_rsa", "authorized_keys", "known_hosts", "config"]))
    q.append(_make_q("Which file stores known host keys?", "known_hosts", ["authorized_keys", "config", "id_rsa.pub", "ssh_host_key"]))
    q.append(_make_q("Which file stores authorized public keys?", "authorized_keys", ["known_hosts", "config", "id_rsa.pub", "ssh_host_key"]))
    q.append(_make_q("What permission should private SSH key have?", "600", ["644", "755", "400", "700"]))
    q.append(_make_q("What permission should .ssh directory have?", "700", ["755", "600", "644", "750"]))
    q.append(_make_q("Which ssh command copies a file?", "scp", all_cmds))
    q.append(_make_q("Which command syncs files remotely?", "rsync", all_cmds))
    q.append(_make_q("What does rsync -avz do?", "Archive + verbose + compress", ["All files + verify", "Append + verify + zip", "Auto + verbose + zip", "Archive + verbose + size"]))
    q.append(_make_q("Which flag with ssh enables verbose?", "-v", ["-V", "-d", "-x", "-D"]))
    q.append(_make_q("What does ssh -X do?", "X11 forwarding", ["Compression", "Encryption", "Tunneling", "Auth forwarding"]))
    q.append(_make_q("What does ssh -L do?", "Local port forwarding", ["Remote forwarding", "Listens on port", "Logs output", "Loads config"]))
    q.append(_make_q("What does ssh -R do?", "Remote port forwarding", ["Local forwarding", "Runs command", "Reverse shell", "Reloads config"]))
    q.append(_make_q("Which command mounts remote via SSH?", "sshfs", all_cmds))
    q.append(_make_q("Which command auto-reconnects tunnels?", "autossh", all_cmds))
    q.append(_make_q("Which command handles roaming connections?", "mosh", all_cmds))
    q.append(_make_q("Which SSH config disables password auth?", "PasswordAuthentication no", ["PermitRootLogin no", "PubkeyAuthentication yes", "ChallengeResponse no", "UsePAM no"]))
    q.append(_make_q("Which SSH config disables root login?", "PermitRootLogin no", ["PasswordAuthentication no", "PubkeyAuthentication yes", "AllowUsers", "DenyUsers"]))
    q.append(_make_q("Which command scans host keys?", "ssh-keyscan", all_cmds))
    q.append(_make_q("What does ssh -J do?", "Jump host connection", ["JSON output", "Join session", "Jump to shell", "Job control"]))
    q.append(_make_q("Where is the SSH server config?", "/etc/ssh/sshd_config", ["/etc/ssh/ssh_config", "~/.ssh/config", "/etc/ssh/known_hosts", "/etc/ssh/ssh_host_key"]))
    q.append(_make_q("Where is the SSH client config?", "/etc/ssh/ssh_config", ["/etc/ssh/sshd_config", "~/.ssh/config", "/etc/ssh/known_hosts", "/etc/ssh/ssh_host_key"]))
    random.shuffle(q)
    return q[:Q_PER_LESSON]

QUESTION_BANKS = {
    0: _nav_questions, 1: _file_questions, 2: _perm_questions,
    3: _proc_questions, 4: _text_questions, 5: _pkg_questions,
    6: _user_questions, 7: _arch_questions, 8: _net_questions,
    9: _ssh_questions,
}

def get_questions(lesson_idx, count=QUIZ_SIZE):
    fn = QUESTION_BANKS.get(lesson_idx)
    if not fn:
        return []
    pool = fn()
    random.shuffle(pool)
    return pool[:count]
