"""Desktop interface. Worker threads communicate exclusively through a queue."""
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from jfcraft_core import atomic_json, Cancelled, load_manifest
from launcher_service import data_dir, load_settings, resource_dir, run_pack, validate_settings, VERSION, sync_catalog, older_manifest, remove_pack, GameProcess, pack_status, featured_pack_id

BG = '#111917'
PANEL = '#1c2823'
TEXT = '#e9e9df'
MUTED = '#a4b5a7'
GOLD = '#d5b775'


class Launcher:
    def __init__(self, root):
        self.root = root
        self.events = queue.Queue()
        self.cancel = threading.Event()
        self.game = GameProcess()
        self.stopping_game = False
        self.worker = None
        self.is_busy = False
        self.pending_catalog = None
        self.started_packs = set()
        self.packs = []
        self.featured_id = featured_pack_id()
        self.featured_selected = False
        self.library_indices = []
        self.library_signature = None
        self.controls = []
        self.settings = load_settings()
        root.title('JFCRAFT • by jamesfimmer')
        self.ui_scale = max(1.0, root.winfo_fpixels('1i') / 96)
        root.geometry(f'{round(1080 * self.ui_scale)}x{round(740 * self.ui_scale)}')
        root.minsize(round(920 * self.ui_scale), round(680 * self.ui_scale))
        root.configure(bg=BG)
        root.protocol('WM_DELETE_WINDOW', self.close)
        style = ttk.Style(root)
        style.theme_use('clam')
        style.configure('TProgressbar', troughcolor=PANEL, background=GOLD, bordercolor=PANEL, lightcolor=GOLD, darkcolor=GOLD)
        style.configure('TCombobox', fieldbackground=PANEL, background=PANEL, foreground=TEXT, arrowcolor=GOLD)
        header = tk.Frame(root, bg=BG)
        header.pack(fill='x', padx=28, pady=(24, 16))
        tk.Label(header, text='JFCRAFT', bg=BG, fg=GOLD, font=('Segoe UI', 25, 'bold')).pack(side='left')
        tk.Label(header, text='ТВОИ МИРЫ. ТВОИ ИСТОРИИ.', bg=BG, fg=MUTED, font=('Segoe UI', 10)).pack(side='left', padx=24)
        tk.Label(header, text=VERSION, bg=BG, fg=MUTED).pack(side='right')
        body = tk.Frame(root, bg=BG)
        body.pack(fill='both', expand=True, padx=28)
        left = tk.Frame(body, bg=PANEL, width=round(260 * self.ui_scale))
        left.pack(side='left', fill='y', padx=(0, 20))
        left.pack_propagate(False)
        tk.Label(left, text='БИБЛИОТЕКА', bg=PANEL, fg=MUTED, font=('Segoe UI', 10, 'bold')).pack(anchor='w', padx=18, pady=(20, 12))
        self.featured_frame = tk.Frame(left, bg=PANEL)
        self.featured_frame.pack(fill='x', padx=14)
        tk.Label(self.featured_frame, text='АКТУАЛЬНАЯ', bg=PANEL, fg=GOLD,
                 font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=(0, 8))
        self.featured_button = self.button(self.featured_frame, '', self.choose_featured)
        self.featured_button.configure(wraplength=220, justify='left', anchor='w',
                                      bg=PANEL, fg=TEXT, activebackground='#425343', activeforeground=TEXT)
        self.featured_button.pack(fill='x')
        tk.Label(self.featured_frame, text='ОСТАЛЬНЫЕ СБОРКИ', bg=PANEL, fg=MUTED,
                 font=('Segoe UI', 9, 'bold')).pack(anchor='w', pady=(22, 8))
        self.library = tk.Listbox(left, bg=PANEL, fg=TEXT, selectbackground='#425343', selectforeground=TEXT,
                                  font=('Segoe UI', 11), relief='flat', borderwidth=0, highlightthickness=0,
                                  activestyle='none', exportselection=False, height=9)
        self.library.pack(fill='x', padx=14)
        self.library.bind('<<ListboxSelect>>', self.select_pack)
        self.controls.append(self.library)
        right = tk.Frame(body, bg=BG)
        right.pack(side='left', fill='both', expand=True)
        self.title = tk.Label(right, text='Выбери сборку', bg=BG, fg=TEXT, font=('Segoe UI', 23, 'bold'), anchor='w')
        self.title.pack(fill='x', pady=(8, 5))
        self.subtitle = tk.Label(right, bg=BG, fg=GOLD, anchor='w', font=('Segoe UI', 10))
        self.subtitle.pack(fill='x')
        self.install_label = tk.Label(right, bg=BG, fg=MUTED, anchor='w', font=('Segoe UI', 10, 'bold'), wraplength=650)
        self.install_label.pack(fill='x', pady=(8, 0))
        self.description = tk.Label(right, bg=BG, fg=MUTED, justify='left', anchor='w', wraplength=670, font=('Segoe UI', 10))
        self.description.pack(fill='x', pady=(12, 18))
        form = tk.Frame(right, bg=PANEL, padx=16, pady=14)
        form.pack(fill='x')
        self.values = {}
        for row, (key, label) in enumerate([('username', 'Никнейм'), ('min_ram', 'Минимум памяти, МБ'), ('max_ram', 'Максимум памяти, МБ')]):
            tk.Label(form, text=label, bg=PANEL, fg=TEXT, anchor='w', font=('Segoe UI', 10)).grid(row=row, column=0, sticky='w', pady=5, padx=(0, 20))
            variable = tk.StringVar(value=str(self.settings.get(key, '')))
            self.values[key] = variable
            entry = tk.Entry(form, textvariable=variable, bg=BG, fg=TEXT, insertbackground=TEXT, relief='flat', font=('Segoe UI', 11))
            entry.grid(row=row, column=1, sticky='ew', ipady=4)
            self.controls.append(entry)
        form.columnconfigure(1, weight=1)
        self.values['java'] = tk.StringVar(value='')
        actions = tk.Frame(right, bg=BG)
        actions.pack(fill='x', pady=(12, 0))
        self.play_button = self.button(actions, 'Играть', lambda: self.start(True), primary=True)
        self.play_button.pack(side='left')
        self.pack_menu = tk.Menu(root, tearoff=False)
        self.pack_menu.add_command(label='Восстановить сборку', command=lambda: self.start(False))
        self.pack_menu.add_command(label='Открыть папку сборки', command=self.open_instance)
        self.pack_menu.add_command(label='Выбрать Java вручную…', command=self.choose_java)
        self.pack_menu.add_command(label='Подбирать Java автоматически', command=lambda: self.values['java'].set(''))
        self.pack_menu.add_separator()
        self.pack_menu.add_command(label='Удалить сборку…', command=self.delete_pack)
        self.menu_button = self.button(actions, '⋯', self.show_pack_menu)
        self.menu_button.pack(side='left', padx=10)
        self.play_button.configure(disabledforeground='#777d76')
        self.cancel_button = tk.Button(actions, text='Отменить', command=self.cancel_install, bg=PANEL, fg=MUTED, relief='flat', padx=12, pady=8, state='disabled')
        self.cancel_button.pack(side='left')
        self.stop_button = tk.Button(actions, text='Закрыть Minecraft', command=self.stop_game,
                                     bg=PANEL, fg=TEXT, relief='flat', padx=12, pady=8)
        self.progress = ttk.Progressbar(right, mode='determinate')
        self.progress.pack(fill='x', pady=(16, 8))
        self.status = tk.Label(right, text='Готов к запуску', bg=BG, fg=MUTED, anchor='w', wraplength=670)
        self.status.pack(fill='x')
        self.console = tk.Text(right, height=6, bg='#0b1210', fg=MUTED, relief='flat', font=('Consolas', 9), state='disabled', wrap='word')
        self.console.pack(fill='both', expand=True, pady=(10, 12))
        footer = tk.Frame(root, bg=BG)
        footer.pack(side='bottom', before=body, fill='x', padx=28, pady=12)
        self.button(footer, 'Логи', lambda: self.open_folder(data_dir() / 'logs')).pack(side='left', padx=10)
        #tk.Label(footer, text='Каждая сборка — отдельный профиль и сохранения', bg=BG, fg=MUTED, font=('Segoe UI', 9)).pack(side='right')
        self.play_button.configure(state='disabled')
        self.root.after(100, self.poll)
        self.catalog_worker = threading.Thread(target=self.load_library, daemon=True)
        self.catalog_worker.start()

    def load_library(self):
        packs = []
        sources = list((resource_dir() / 'packs').glob('*.json')) + list((data_dir() / 'manifests').glob('*.json'))
        for source in sources:
            try:
                packs.append(load_manifest(source))
            except Exception as error:
                self.events.put(('catalog_log', f'Не удалось прочитать {source.name}: {error}'))
        self.events.put(('local_library', packs))
        self.refresh_library()

    def refresh_library(self):
        try:
            packs = sync_catalog(lambda message: None, persist=False)
            self.events.put(('catalog', packs))
        except Exception as error:
            self.events.put(('catalog_log', f'Каталог недоступен; используется сохранённая библиотека. {error}'))

    def apply_catalog(self):
        if self.pending_catalog is None or self.is_busy:
            return
        selected = self.current()['id'] if self.selected_indices() else None
        java = self.values['java'].get()
        if hasattr(self.pending_catalog, 'featured'):
            self.featured_id = self.pending_catalog.featured
            atomic_json(data_dir() / 'catalog.json', {'featured': self.featured_id})
        for pack in self.pending_catalog:
            cached = data_dir() / 'manifests' / (pack['id'] + '.json')
            try:
                if cached.exists():
                    local = load_manifest(cached)
                    if pack['id'] in self.started_packs or older_manifest(pack, local):
                        pack = local
                self.add_pack(pack, render=False)
                atomic_json(cached, pack)
            except Exception as error:
                self.log(f'Не удалось сохранить описание {pack["id"]}: {error}')
        self.pending_catalog = None
        self.render_library()
        if self.packs:
            index = next((i for i, p in enumerate(self.packs) if p['id'] == selected), 0)
            self.library.selection_clear(0, 'end')
            self.choose_index(index)
            self.select_pack()
            if selected:
                self.values['java'].set(java)
        self.log('Библиотека сборок обновлена с GitHub.')

    def button(self, parent, text, command, primary=False):
        button = tk.Button(parent, text=text, command=command, bg=GOLD if primary else '#2c3c33', fg=BG if primary else TEXT,
                           activebackground='#e3cd9a', activeforeground=BG, relief='flat', padx=12, pady=8,
                           cursor='hand2', font=('Segoe UI', 10, 'bold' if primary else 'normal'))
        self.controls.append(button)
        return button

    def add_pack(self, pack, render=True):
        existing = next((i for i, p in enumerate(self.packs) if p['id'] == pack['id']), None)
        if existing is not None:
            if older_manifest(pack, self.packs[existing]):
                return
            self.packs[existing] = pack

        else:
            self.packs.append(pack)
        if render:
            self.render_library()


    def selected_indices(self):
        rows = self.library.curselection()
        if rows and rows[0] < len(self.library_indices):
            return (self.library_indices[rows[0]],)
        if self.featured_selected:
            return tuple(i for i, p in enumerate(self.packs) if p['id'] == self.featured_id)[:1]
        return ()

    def choose_index(self, index):
        self.library.selection_clear(0, 'end')
        self.featured_selected = self.packs[index]['id'] == self.featured_id
        if not self.featured_selected and index in self.library_indices:
            self.library.selection_set(self.library_indices.index(index))

    def choose_featured(self):
        if self.is_busy:
            return
        index = next((i for i, p in enumerate(self.packs) if p['id'] == self.featured_id), None)
        if index is not None:
            self.choose_index(index)
            self.select_pack()

    def render_library(self):
        rows = []
        for index, pack in enumerate(self.packs):
            kind, _ = pack_status(pack, data_dir() / 'instances' / pack['id'])
            symbol = {'missing': '○', 'installed': '✓', 'update': '↑', 'repair': '!'}[kind]
            rows.append((index, pack['id'], f"{symbol}  {pack['name']}"))
        signature = (self.featured_id, tuple(rows))
        if signature == self.library_signature:
            return
        self.library_signature = signature
        selected = self.selected_indices()
        self.library.delete(0, 'end')
        self.library_indices = []
        found = False
        for index, pack_id, label in rows:
            if pack_id == self.featured_id:
                found = True
                self.featured_button.configure(text=label)
            else:
                self.library_indices.append(index)
                self.library.insert('end', label)
        if found:
            self.featured_frame.pack(fill='x', padx=14, before=self.library)
        else:
            self.featured_frame.pack_forget()
        if selected:
            self.choose_index(selected[0])

    def current(self):
        selection = self.selected_indices()
        if not selection:
            raise ValueError('Выбери сборку из библиотеки')
        return self.packs[selection[0]]

    def select_pack(self, event=None):
        try:
            pack = self.current()
        except ValueError:
            return
        self.title.configure(text=pack['name'])
        self.subtitle.configure(text=f"Minecraft {pack['minecraft']}   /   Forge {pack['forge'].split('-')[1]}   /   Java {pack['java']}   /   {pack['version']}")
        size = sum(f['size'] for f in pack['files']) / 1024**2
        self.description.configure(text=pack.get('description', f"{len(pack['files'])} файлов • {size:.0f} МБ"))
        chosen = self.settings.get('java_by_pack', {}).get(pack['id'], '')
        self.values['java'].set(chosen)
        self.update_actions()

    def update_actions(self):
        selected = self.selected_indices()
        featured_active = bool(selected and self.packs[selected[0]]['id'] == self.featured_id)
        self.featured_button.configure(bg='#425343' if featured_active else PANEL)
        self.render_library()
        if selected:
            pack = self.packs[selected[0]]
            kind, text = pack_status(pack, data_dir() / 'instances' / pack['id'])
            self.installed = kind in ('installed', 'update')
            self.install_label.configure(text=text, fg=GOLD if kind in ('update', 'repair') else '#8bc99a' if kind == 'installed' else MUTED)
        self.play_button.configure(state='disabled' if self.is_busy or not self.packs else 'normal', bg=GOLD)

    def show_pack_menu(self):
        if not self.is_busy:
            try:
                self.pack_menu.tk_popup(self.menu_button.winfo_rootx(),
                                        self.menu_button.winfo_rooty() + self.menu_button.winfo_height())
            finally:
                self.pack_menu.grab_release()

    def delete_pack(self):
        if self.is_busy:
            return
        pack = self.current()
        if not messagebox.askyesno('Удалить сборку?',
                f"Удалить установленную сборку «{pack['name']}»?\n\n"
                'Миры и остальные файлы сохранятся в резервной копии. '
                'Место на диске не освободится. '
                'Сборка останется в библиотеке для повторной установки.'):
            return
        try:
            backup = remove_pack(pack['id'])
            self.log('Сборка удалена из установленных. Резервная копия: ' + str(backup))
        except Exception as error:
            messagebox.showerror('Не удалось удалить сборку', str(error))
        self.update_actions()

    def log(self, message):
        logging.info(message)
        self.console.configure(state='normal')
        self.console.insert('end', message + '\n')
        if int(self.console.index('end-1c').split('.')[0]) > 500:
            self.console.delete('1.0', '100.0')
        self.console.see('end')
        self.console.configure(state='disabled')

    def choose_java(self):
        path = filedialog.askopenfilename(title='Выбери java.exe', filetypes=[('Java', 'java.exe'), ('Все файлы', '*')])
        if path:
            self.values['java'].set(path)

    def import_manifest(self):
        path = filedialog.askopenfilename(title='Описание сборки', filetypes=[('Манифест', '*.json')])
        if path:
            self.import_source(path)

    def import_url(self):
        url = simpledialog.askstring('Добавить сборку', 'HTTPS-ссылка на manifest.json выпуска:')
        if url:
            if not url.startswith('https://'):
                messagebox.showerror('Ссылка', 'Нужна HTTPS-ссылка')
                return
            self.import_source(url)

    def import_source(self, source):
        self.busy(True)
        def work():
            try:
                pack = load_manifest(source)
                if str(source).startswith('https://'):
                    pack['update_url'] = source
                target = data_dir() / 'manifests' / (pack['id'] + '.json')
                atomic_json(target, pack)
                self.events.put(('pack', (pack, str(target))))
            except Exception as error:
                self.events.put(('error', str(error)))
            finally:
                self.events.put(('done', None))
        self.worker = threading.Thread(target=work, daemon=False)
        self.worker.start()

    def busy(self, value):
        self.is_busy = value
        for control in self.controls:
            control.configure(state='disabled' if value else 'normal')
        self.cancel_button.configure(state='normal' if value else 'disabled')
        if not value:
            self.update_actions()

    def start(self, play):
        if self.is_busy:
            return
        self.update_actions()
        try:
            pack = self.current()
            self.started_packs.add(pack['id'])
            settings = validate_settings(dict(self.settings, **{key: value.get().strip() for key, value in self.values.items()}))
            settings['pack'] = pack['id']
            settings.setdefault('java_by_pack', {})[pack['id']] = settings['java']
            atomic_json(data_dir() / 'settings.json', settings)
            self.settings = settings
        except Exception as error:
            messagebox.showerror('Проверь настройки', str(error))
            return
        self.cancel.clear()
        self.progress['value'] = 0
        self.busy(True)
        self.status.configure(text='Подготовка сборки…')
        def work():
            try:
                run_pack(pack, settings, play, lambda m: self.events.put(('log', m)),
                         lambda v, t: self.events.put(('progress', (v, t))), self.cancel, self.game)
                self.events.put(('log', 'Готово'))
            except Cancelled:
                self.events.put(('log', 'Установка отменена'))
            except Exception as error:
                logging.exception('Операция завершилась ошибкой')
                self.events.put(('error', str(error)))
            finally:
                self.events.put(('done', None))
        self.worker = threading.Thread(target=work, daemon=False)
        self.worker.start()

    def cancel_install(self):
        self.cancel.set()
        self.status.configure(text='Отмена после текущего шага. Запущенная игра продолжит работать.')
        self.cancel_button.configure(state='disabled')

    def stop_game(self):
        if self.stopping_game or not self.game.running():
            return
        if not messagebox.askyesno('Принудительно закрыть Minecraft?',
                'Несохранённый прогресс может потеряться. Завершить игру?', parent=self.root):
            return
        self.stopping_game = True
        self.stop_button.configure(state='disabled')
        def work():
            try:
                self.game.stop()
            except Exception as error:
                self.events.put(('error', str(error)))
            finally:
                self.events.put(('stop_done', None))
        threading.Thread(target=work, daemon=False).start()

    def poll(self):
        for _ in range(100):
            try:
                kind, payload = self.events.get_nowait()
            except queue.Empty:
                break
            if kind in ('log', 'error'):
                self.log(payload)
                self.status.configure(text=payload)
                if kind == 'error':
                    messagebox.showerror('Не удалось завершить операцию', payload)
            elif kind == 'progress':
                value, total = payload
                self.progress['value'] = value / max(total, 1) * 100
            elif kind == 'catalog_pack':
                selected_id = self.current()['id'] if self.selected_indices() else None
                self.add_pack(payload)
                if selected_id:
                    self.choose_index(next(i for i, p in enumerate(self.packs) if p['id'] == selected_id))
                    self.select_pack()
            elif kind == 'pack':
                self.busy(False)
                pack, path = payload
                self.add_pack(pack)
                if path not in self.settings['sources']:
                    self.settings['sources'].append(path)
                atomic_json(data_dir() / 'settings.json', self.settings)
                self.library.selection_clear(0, 'end')
                self.choose_index(next(i for i, p in enumerate(self.packs) if p['id'] == pack['id']))
                self.select_pack()
            elif kind == 'done':
                selected = self.selected_indices()
                if selected:
                    pack = self.packs[selected[0]]
                    cached = data_dir() / 'manifests' / (pack['id'] + '.json')
                    try:
                        latest = load_manifest(cached)
                        if latest['id'] == pack['id']:
                            self.add_pack(latest)
                            self.choose_index(selected[0])
                            java = self.values['java'].get()
                            self.select_pack()
                            self.values['java'].set(java)
                    except (OSError, ValueError, KeyError):
                        pass
                self.busy(False)
            elif kind == 'stop_done':
                self.stopping_game = False
            elif kind == 'local_library':
                for pack in payload:
                    self.add_pack(pack, render=False)
                self.render_library()
                if self.packs:
                    index = next((i for i, p in enumerate(self.packs) if p['id'] == self.settings.get('pack')),
                                 next((i for i, p in enumerate(self.packs) if p['id'] == self.featured_id), 0))
                    self.choose_index(index)
                    self.select_pack()
            elif kind == 'catalog':
                self.pending_catalog = payload
            elif kind == 'catalog_log':
                self.log(payload)
        self.apply_catalog()
        if not self.stopping_game:
            if self.game.running():
                self.cancel_button.pack_forget()
                self.stop_button.pack(side='left')
                self.stop_button.configure(state='normal')
            else:
                self.stop_button.pack_forget()
                self.cancel_button.pack(side='left')
        self.root.after(100, self.poll)

    def open_folder(self, path):
        path.mkdir(parents=True, exist_ok=True)
        if os.name == 'nt':
            os.startfile(path)

    def open_instance(self):
        try:
            self.open_folder(data_dir() / 'instances' / self.current()['id'])
        except ValueError as error:
            messagebox.showinfo('Сборка', str(error))

    def close(self):
        if self.worker and self.worker.is_alive():
            messagebox.showinfo('Операция ещё выполняется', 'Дождись завершения установки или закрой Minecraft. Установку можно отменить кнопкой «Отменить».')
            return
        self.root.destroy()


def enable_high_dpi():
    """Opt out of Windows bitmap scaling before creating any Tk window."""
    if os.name == 'nt':
        import ctypes
        try:
            if ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4)):
                return
        except (AttributeError, OSError):
            pass
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, OSError):
            ctypes.windll.user32.SetProcessDPIAware()


def startup():
    enable_high_dpi()
    logs = data_dir() / 'logs'
    logs.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(logs / 'launcher.log', maxBytes=2_000_000, backupCount=3, encoding='utf-8')
    logging.basicConfig(level=logging.INFO, handlers=[handler], format='%(asctime)s %(levelname)s %(message)s')
    root = tk.Tk()
    try:
        Launcher(root)
    except Exception as error:
        logging.exception('Ошибка запуска')
        messagebox.showerror('JFCRAFT', str(error))
        root.destroy()
        return
    root.mainloop()
