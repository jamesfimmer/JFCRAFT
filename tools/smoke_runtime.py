"""Install a clean legacy Forge runtime in workspace output for verification."""
import json
from pathlib import Path
import sys
import threading
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from launcher_service import ensure_forge, check_java

root = Path(__file__).resolve().parents[1] / 'output' / 'runtime-smoke'
pack = dict(minecraft='1.7.10', forge='1.7.10-10.13.4.1614-1.7.10', installed_version='1.7.10-Forge10.13.4.1614-1.7.10')
java = check_java('C:/Program Files/Java/jre1.8.0_491/bin/java.exe', 8)
ensure_forge(pack, root, java, print, threading.Event())
import minecraft_launcher_lib as mc
command = mc.command.get_minecraft_command(pack['installed_version'], str(root), dict(username='TestPlayer', uuid='00000000-0000-3000-8000-000000000000', token='0', executablePath=java))
print('COMMAND_READY', len(command), 'arguments')
