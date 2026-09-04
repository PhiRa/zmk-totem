import json, os, sys

KEYS = (
    [chr(c) for c in range(ord('a'), ord('z')+1)] +
    ["1","2","3","4","5","6","7","8","9","0"] +
    ["return_or_enter","escape","delete_or_backspace","delete_forward","tab","spacebar",
     "hyphen","equal_sign","open_bracket","close_bracket","backslash","non_us_pound",
     "semicolon","quote","grave_accent_and_tilde","comma","period","slash","non_us_backslash"] +
    ["f%d" % i for i in range(1,13)] +
    ["print_screen","scroll_lock","pause","insert","home","page_up","end","page_down",
     "right_arrow","left_arrow","down_arrow","up_arrow"] +
    ["keypad_num_lock","keypad_slash","keypad_asterisk","keypad_hyphen","keypad_plus",
     "keypad_enter","keypad_equal_sign","keypad_period"] +
    ["keypad_%d" % i for i in range(0,10)]
)

VAR = "active_keyboard"

DEVICES = {
    "corne": {
        "label": "Corne",
        "identifiers": [{"vendor_id": 7504, "product_id": 24926}],
        "input_source": "^com\\.apple\\.keylayout\\.UnicodeHexInput$",
    },
    "builtin": {
        "label": "built-in",
        "identifiers": [{"is_built_in_keyboard": True}],
        "input_source": "^com\\.apple\\.keylayout\\.Danish$",
    },
}

manipulators = []
for name, dev in DEVICES.items():
    for key in KEYS:
        manipulators.append({
            "type": "basic",
            "from": {"key_code": key, "modifiers": {"optional": ["any"]}},
            "to": [
                {"select_input_source": {"input_source_id": dev["input_source"]}},
                {"set_variable": {"name": VAR, "value": name}},
                {"key_code": key},
            ],
            "conditions": [
                {"type": "device_if", "identifiers": dev["identifiers"]},
                {"type": "variable_unless", "name": VAR, "value": name},
            ],
        })

rule = {
    "title": "Per-keyboard input source (Corne / built-in)",
    "rules": [{
        "description": "Switch to Unicode Hex Input when typing on the Corne, Danish when typing on the built-in keyboard",
        "manipulators": manipulators,
    }],
}

def write(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(rule, f, indent=2)
        f.write("\n")
    print("wrote", path, "-", len(manipulators), "manipulators")


FILENAME = "per-keyboard-input-source.json"
write(os.path.join(os.path.dirname(os.path.abspath(__file__)), FILENAME))

if "--install" in sys.argv:
    write(os.path.expanduser(
        "~/.config/karabiner/assets/complex_modifications/" + FILENAME))
