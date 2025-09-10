import logging
from pynput import keyboard
import pygame

from . import config
from . import utils

def get_controller_direction(engine):
    dx, dy = 0, 0
    deadzone = 0.2

    for joystick in engine.joysticks:
        # Left stick
        axis_x = joystick.get_axis(0)
        axis_y = joystick.get_axis(1)

        if abs(axis_x) > deadzone:
            dx += axis_x * config.X_SPD * 5
        if abs(axis_y) > deadzone:
            dy -= axis_y * config.X_SPD * 5  # invert if needed

        # D-pad (hat)
        hat_x, hat_y = joystick.get_hat(0)
        dx += hat_x * config.X_SPD * 5
        dy += hat_y * config.X_SPD * 5

    return dx, dy

def _do_speed(engine):
    try:
        x_addr = utils.resolve_pointer_chain(engine.process, config.x_base, config.x_offsets)
        if x_addr:
            cx = engine.process.read_process_memory(x_addr, float, 4)
            
            # Keyboard input
            if keyboard.Key.left in engine.pressed_keys:  cx -= config.X_SPD
            if keyboard.Key.right in engine.pressed_keys: cx += config.X_SPD

            # Controller input
            dx, _ = get_controller_direction(engine)
            cx += dx * 0.10

            engine.process.write_process_memory(x_addr, float, 4, cx)
    except Exception as e: 
        logging.error(f"Error in _do_speed: {e}")

def _do_flight(engine):
    try:
        y_addr = utils.resolve_pointer_chain(engine.process, config.y_base, config.y_offsets)
        if y_addr:
            cy = engine.process.read_process_memory(y_addr, float, 4)

            # Keyboard input
            if keyboard.Key.up in engine.pressed_keys:    cy += 1
            if keyboard.Key.down in engine.pressed_keys:  cy -= 1

            # Controller input
            _, dy = get_controller_direction(engine)
            cy += dy * 0.10

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

            # Keyboard input
            if keyboard.Key.left in engine.pressed_keys:  cx -= config.X_SPD
            if keyboard.Key.right in engine.pressed_keys: cx += config.X_SPD
            if keyboard.Key.up in engine.pressed_keys:    cy += .5
            if keyboard.Key.down in engine.pressed_keys:  cy -= .5

            # Controller input
            dx, dy = get_controller_direction(engine)
            cx += dx * 0.10
            cy += dy * 0.10

            engine.process.write_process_memory(x_addr, float, 4, cx)
            engine.process.write_process_memory(y_addr, float, 4, cy)
    except Exception as e: 
        logging.error(f"Error in _do_superfly: {e}")

"""
def save_things_ad(engine):
    try:
        health = engine.process.read_process_memory(utils.resolve_pointer_chain(engine.process, config.health_base, config.health_offsets), int, 4)
        if health <= 0:
            engine.process.write_process_memory(utils.resolve_pointer_chain(engine.process, config.rosary_base, config.rosary_offsets), int, 4, engine.rosarys)
            engine.process.write_process_memory(utils.resolve_pointer_chain(engine.process, config.shards_base, config.shards_offsets), int, 4, engine.shells)
            return
        
        engine.rosarys = engine.process.read_process_memory(utils.resolve_pointer_chain(engine.process, config.rosary_base, config.rosary_offsets), int, 4)
        engine.shells = engine.process.read_process_memory(utils.resolve_pointer_chain(engine.process, config.shards_base, config.shards_offsets), int, 4)
    except Exception as e:
        logging.error(f"Error in save_things_ad: {e}")

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
        if engine.do_save_items.get(): save_things_ad(engine)
    except Exception as e:
        logging.error(f"Error in cheat loop: {e}")
    engine.root.after(20, lambda: _cheat_loop(engine))
""