"""Exercise the real Tk window without downloading or launching Minecraft."""
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ['JFCRAFT_HOME'] = str(Path(__file__).resolve().parents[1] / 'output' / 'ui-smoke')
import tkinter as tk
from jfcraft_ui import Launcher

root = tk.Tk()
app = Launcher(root)
root.update()
assert len(app.packs) == 5, len(app.packs)
for i in range(len(app.packs)):
    app.library.selection_clear(0, 'end')
    app.library.selection_set(i)
    app.select_pack()
    assert app.title.cget('text') == app.packs[i]['name']
app.busy(True)
assert app.library.cget('state') == 'disabled'
app.busy(False)
assert app.library.cget('state') == 'normal'
assert app.console.winfo_height() > 30
for width, height in [(1080, 740), (920, 680)]:
    root.geometry(f'{width}x{height}')
    root.update()
    for widget in app.controls:
        assert widget.winfo_rooty() + widget.winfo_height() <= root.winfo_rooty() + root.winfo_height(), str(widget)
print('UI_OK: five packs, profile switching, busy state, minimum window size')
root.destroy()
