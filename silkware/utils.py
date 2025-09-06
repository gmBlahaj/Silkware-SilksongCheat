import logging
import sys
import subprocess

if sys.platform == "win32":
    try:
        import win32api
        import win32process
        import win32con
    except ImportError:
        print("The 'pywin32' library is required for Windows. Please install it by running: pip install pywin32")
        sys.exit(1)

def get_process_name(pid):
    if sys.platform.startswith("linux"):
        try:
            with open(f"/proc/{pid}/comm", 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None
    elif sys.platform == "win32":
        try:
            h_process = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
            if h_process:
                try:
                    exe_path = win32process.GetModuleFileNameEx(h_process, 0)
                    return exe_path.split('\\')[-1]
                finally:
                    win32api.CloseHandle(h_process)
        except Exception:
            return None
    return None

def get_module_base_address(process, module_name):
    if sys.platform.startswith("linux"):
        pid = process.pid
        try:
            with open(f"/proc/{pid}/maps", 'r') as f:
                for line in f:
                    if module_name in line:
                        return int(line.split('-')[0], 16)
        except FileNotFoundError:
            return None
        return None
    elif sys.platform == "win32":
        for module in process.list_modules():
            if module.name.lower() == module_name.lower():
                return module.base_address
        return None
    return None

def resolve_pointer_chain(process, base, offsets):
    try:
        addr = process.read_process_memory(base, int, 8)
        logging.info(f"Resolving pointer chain: base={hex(base)}, initial_read={hex(addr)}")
        for i, offset in enumerate(offsets[:-1]):
            addr = process.read_process_memory(addr + offset, int, 8)
            logging.info(f"  step {i+1}: offset={hex(offset)}, next_addr={hex(addr)}")
        final_addr = addr + offsets[-1]
        logging.info(f"  final step: offset={hex(offsets[-1])}, final_addr={hex(final_addr)}")
        return final_addr
    except Exception as e:
        logging.error(f"Could not resolve pointer chain: {e}")
        return None

def get_pid_by_name(process_name):
    if sys.platform.startswith("linux"):
        try:
            pid_str = subprocess.check_output(["pidof", "-s", process_name]).strip()
            return int(pid_str)
        except (subprocess.CalledProcessError, ValueError, FileNotFoundError):
            return None
    elif sys.platform == "win32":
        pids = win32process.EnumProcesses()
        for pid_candidate in pids:
            name = get_process_name(pid_candidate)
            if name and process_name.lower() in name.lower():
                return pid_candidate
    return None
