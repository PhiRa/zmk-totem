# Karabiner-Elements: per-keyboard input source

A complex modification for [Karabiner-Elements](https://karabiner-elements.pqrs.org/) that
switches the macOS input source based on which keyboard is being typed on:

| Keyboard            | Input source      |
| ------------------- | ----------------- |
| Corne (ZMK)         | Unicode Hex Input |
| Built-in MacBook    | Danish            |

## Installation

Copy the rule into the Karabiner assets directory and enable it in the UI:

```sh
cp per-keyboard-input-source.json ~/.config/karabiner/assets/complex_modifications/
```

Then open Karabiner-Elements → Settings → Complex Modifications → Add rule, and enable
"Switch to Unicode Hex Input when typing on the Corne, Danish when typing on the built-in
keyboard".

Both input sources must already be enabled in System Settings → Keyboard → Input Sources,
otherwise `select_input_source` has nothing to switch to.

## Regenerating

`per-keyboard-input-source.json` is generated; edit `generate.py` rather than the JSON.

```sh
python3 generate.py            # rewrite the JSON in this directory
python3 generate.py --install  # also write it into ~/.config/karabiner/...
```

## How it works

Karabiner has no way to observe a key without consuming it — `"from": {"any": "key_code"}`
matches every key but cannot re-emit the key that triggered it. The rule therefore contains
one manipulator per key code (97 keys × 2 devices), each of which re-emits itself:

```
from:       key X, modifiers optional any
conditions: device_if(<Corne | built-in>) AND variable_unless(active_keyboard, <name>)
to:         [select_input_source, set_variable active_keyboard, key X]
```

The `variable_unless` guard means a manipulator only matches on the first keystroke after
switching keyboards, so `select_input_source` is not invoked on every keypress.

## Adapting to other hardware

The Corne is matched by the USB identifiers ZMK uses by default, `vendor_id 7504`
(0x1D50) and `product_id 24926` (0x615E). Find the values for your own hardware in
Karabiner-EventViewer → Devices, and edit the `DEVICES` table in `generate.py`.

Bluetooth and USB connections can enumerate with different identifiers; if so, add both as
separate entries in the device's `identifiers` list. Matching on `vendor_id` alone will
cover every ZMK keyboard, including the Totem in this repository.

## Known limitations

- The first keystroke after switching keyboards can be delivered before macOS has finished
  applying the new layout, so that one character is occasionally typed in the old layout.
- Modifier keys alone (shift, command, control, option, caps lock) do not trigger a switch.
- Switching input source manually, e.g. with ctrl+space, leaves the `active_keyboard`
  variable stale until the other keyboard is used again.
