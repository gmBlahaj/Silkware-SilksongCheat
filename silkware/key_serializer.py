from pynput import keyboard

def key_to_str(key):
   # pyinput is kinda shit but i need root for keyboard on linux so we doing this now :shrug:
    if isinstance(key, keyboard.KeyCode):
        return key.char
    elif isinstance(key, keyboard.Key):
        return key.name
    return None

def str_to_key(s):
    # the ol switcheroo
    if len(s) == 1:
        return keyboard.KeyCode.from_char(s)
    else:
        try:
            return keyboard.Key[s]
        except KeyError:
            return None
