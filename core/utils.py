import platform, shutil, subprocess, os, pwd, grp, socket

def get_system_info():
    info = {}
    try:
        info["os"] = platform.system()
        info["os_release"] = platform.release()
        info["hostname"] = socket.gethostname()
        info["arch"] = platform.machine()
        info["python"] = platform.python_version()
        info["user"] = pwd.getpwuid(os.getuid()).pw_name
        info["cwd"] = os.getcwd()
        try:
            info["shell"] = os.environ.get("SHELL", "unknown")
        except:
            info["shell"] = "unknown"
        info["cpu_count"] = os.cpu_count()
        try:
            total, used, free = shutil.disk_usage("/")
            info["disk_total"] = f"{total // (2**30)}G"
            info["disk_free"] = f"{free // (2**30)}G"
        except:
            pass
    except:
        pass
    return info

def get_terminal_size():
    try:
        return shutil.get_terminal_size()
    except:
        return (80, 24)
