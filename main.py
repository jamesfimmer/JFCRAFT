from launcher_ui import startup

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3 and sys.argv[1] == '--smoke-test':
        import tkinter as tk
        from pathlib import Path
        from jfcraft_ui import Launcher, enable_high_dpi
        from jfcraft_core import atomic_json
        enable_high_dpi()
        root = tk.Tk()
        root.withdraw()
        app = Launcher(root)
        root.update_idletasks()
        atomic_json(Path(sys.argv[2]), {'ok': True, 'packs': [p['id'] for p in app.packs]})
        root.destroy()
    else:
        startup()
