import logging
import sys

if sys.platform == "win32":
    import psutil

def get_process_name(pid):
    if sys.platform.startswith("linux"):
        try:
            with open(f"/proc/{pid}/comm", 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None
    elif sys.platform == "win32":
        try:
            return psutil.Process(pid).name()
        except psutil.NoSuchProcess:
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