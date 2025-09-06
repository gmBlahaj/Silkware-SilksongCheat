import logging
from pynput import keyboard

from . import config
from . import utils

def _do_speed(engine):
    try:
        x_addr = utils.resolve_pointer_chain(engine.process, config.x_base, config.x_offsets)
        if x_addr:
            cx = engine.process.read_process_memory(x_addr, float, 4)
            if keyboard.Key.left in engine.pressed_keys:  cx -= config.X_SPD
            if keyboard.Key.right in engine.pressed_keys: cx += config.X_SPD
            engine.process.write_process_memory(x_addr, float, 4, cx)
    except Exception as e: 
        logging.error(f"Error in _do_speed: {e}")

def _do_flight(engine):
    try:
        y_addr = utils.resolve_pointer_chain(engine.process, config.y_base, config.y_offsets)
        if y_addr:
            cy = engine.process.read_process_memory(y_addr, float, 4)
            if keyboard.Key.up in engine.pressed_keys:    cy += 1
            if keyboard.Key.down in engine.pressed_keys:  cy -= 1
            engine.process.write_process_memory(y_addr, float, 4, cy)
    except Exception as e: 
        logging.error(f"Error in _do_flight: {e}")

def toggle_superfly(engine):
    if engine.superfly.get():
        logging.info("Superfly enabled")
        try:
            if engine.superfly_orig_bytes is None:
                engine.superfly_orig_bytes = engine.process.read_process_memory(config.superfly_addr, bytes, 5)
            engine.process.write_process_memory(config.superfly_addr, bytes, 5, b'\x90' * 5)
        except Exception as e:
            logging.error(f"Error enabling No Clip: {e}")
    else:
        logging.info("Superfly disabled")
        try:
            if engine.superfly_orig_bytes:
                engine.process.write_process_memory(config.superfly_addr, bytes, 5, engine.superfly_orig_bytes)
        except Exception as e:
            logging.error(f"Error disabling No Clip: {e}")

def _do_superfly(engine):
    try:
        x_addr = utils.resolve_pointer_chain(engine.process, config.x_base, config.x_offsets)
        y_addr = utils.resolve_pointer_chain(engine.process, config.y_base, config.y_offsets)
        if x_addr and y_addr:
            cx = engine.process.read_process_memory(x_addr, float, 4)
            cy = engine.process.read_process_memory(y_addr, float, 4)
            if keyboard.Key.left in engine.pressed_keys:  cx -= config.X_SPD
            if keyboard.Key.right in engine.pressed_keys: cx += config.X_SPD
            if keyboard.Key.up in engine.pressed_keys:    cy += .5
            if keyboard.Key.down in engine.pressed_keys:  cy -= .5
            engine.process.write_process_memory(x_addr, float, 4, cx)
            engine.process.write_process_memory(y_addr, float, 4, cy)
    except Exception as e: 
        logging.error(f"Error in _do_superfly: {e}")

def _cheat_loop(engine):
    try:
        if engine.do_rosary.get():
            addr = utils.resolve_pointer_chain(engine.process, config.rosary_base, config.rosary_offsets)
            if addr:
                old_value = engine.process.read_process_memory(addr, int, 4)
                engine.process.write_process_memory(addr, int, 4, 9999)
                new_value = engine.process.read_process_memory(addr, int, 4)
                logging.info(f"Rosary Beads: addr={hex(addr)}, old={old_value}, new={new_value}")
        if engine.do_shards.get():
            addr = utils.resolve_pointer_chain(engine.process, config.shards_base, config.shards_offsets)
            if addr:
                old_value = engine.process.read_process_memory(addr, int, 4)
                engine.process.write_process_memory(addr, int, 4, 9999)
                new_value = engine.process.read_process_memory(addr, int, 4)
                logging.info(f"Shell Shards: addr={hex(addr)}, old={old_value}, new={new_value}")
        if engine.do_health.get():
            addr = utils.resolve_pointer_chain(engine.process, config.health_base, config.health_offsets)
            if addr:
                old_value = engine.process.read_process_memory(addr, int, 4)
                engine.process.write_process_memory(addr, int, 4, 10)
                new_value = engine.process.read_process_memory(addr, int, 4)
                logging.info(f"Health: addr={hex(addr)}, old={old_value}, new={new_value}")
        if engine.do_soul.get():
            addr = utils.resolve_pointer_chain(engine.process, config.soul_base, config.soul_offsets)
            if addr:
                old_value = engine.process.read_process_memory(addr, int, 4)
                engine.process.write_process_memory(addr, int, 4, 18)
                new_value = engine.process.read_process_memory(addr, int, 4)
                logging.info(f"Soul: addr={hex(addr)}, old={old_value}, new={new_value}")
        if engine.speed.get(): _do_speed(engine)
        if engine.flight.get(): _do_flight(engine)
        if engine.superfly.get(): _do_superfly(engine)
    except Exception as e:
        logging.error(f"Error in cheat loop: {e}")
    engine.root.after(20, lambda: _cheat_loop(engine))