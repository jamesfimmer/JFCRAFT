"""Exercise the real Tk window without downloading or launching Minecraft."""
import os
from pathlib import Path
import sys
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ['JFCRAFT_HOME'] = str(Path(__file__).resolve().parents[1] / 'output' / 'ui-smoke')
import tkinter as tk
from jfcraft_ui import Launcher, enable_high_dpi
from jfcraft_core import atomic_json
from launcher_service import data_dir

enable_high_dpi()
root = tk.Tk()
app = Launcher(root)
root.update()
assert len(app.packs) == 5, len(app.packs)
for i in range(len(app.packs)):
    app.library.selection_clear(0, 'end')
    app.library.selection_set(i)
    app.select_pack()
    assert app.title.cget('text') == app.packs[i]['name']
    assert app.play_button.cget('state') == 'normal'
app.busy(True)
assert app.library.cget('state') == 'disabled'
app.busy(False)
assert app.library.cget('state') == 'normal'
assert app.play_button.cget('state') == 'normal'
with patch('jfcraft_ui.sync_catalog', return_value=[]), patch('jfcraft_ui.run_pack') as run:
    app.start(True)
    app.worker.join(timeout=5)
    assert not app.worker.is_alive()
    assert [call.args[2] for call in run.call_args_list] == [True]
    app.poll()
pack = app.current()
instance = data_dir() / 'instances' / pack['id']
state = instance / '.jfcraft-state.json'
version = instance / 'versions' / pack['installed_version'] / (pack['installed_version'] + '.json')
try:
    atomic_json(state, pack)
    atomic_json(version, {})
    app.update_actions()
    assert app.play_button.cget('state') == 'normal'
    with patch('jfcraft_ui.sync_catalog', side_effect=AssertionError('Offline launch contacted catalog')), patch('jfcraft_ui.run_pack') as run:
        app.start(True)
        app.worker.join(timeout=5)
        assert [call.args[2] for call in run.call_args_list] == [True]
        app.poll()
    app.busy(True)
    app.update_actions()
    assert app.play_button.cget('state') == 'disabled'
    app.busy(False)
    assert app.play_button.cget('state') == 'normal'
finally:
    state.unlink(missing_ok=True)
    version.unlink(missing_ok=True)
    app.update_actions()
assert app.console.winfo_height() > 30
for width, height in [(1080, 740), (920, 680)]:
    root.geometry(f'{round(width * app.ui_scale)}x{round(height * app.ui_scale)}')
    root.update()
    for widget in app.controls:
        assert widget.winfo_rooty() + widget.winfo_height() <= root.winfo_rooty() + root.winfo_height(), str(widget)
print('UI_OK: five packs, profile switching, busy state, minimum window size')
root.destroy()
