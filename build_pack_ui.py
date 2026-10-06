"""Run directly to create or update a pack manifest and its catalog entry."""
import ctypes
import json
from pathlib import Path
import queue
import re
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from urllib.parse import unquote, urlsplit

from jfcraft_core import atomic_json, load_manifest
from tools.build_pack import build

ROOT = Path(__file__).resolve().parent


def create_pack(root, source, fields, register=True):
    """Use repository-relative sources so generated URLs match committed files."""
    root, source = Path(root).resolve(), Path(source).resolve()
    downloads = (root / 'download-files').resolve()
    if not source.is_dir() or source == downloads or not source.is_relative_to(downloads):
        raise ValueError('Выбери папку конкретной сборки внутри download-files проекта.')
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}', fields['id']):
        raise ValueError('ID: от 1 до 64 символов, маленькие латинские буквы, цифры, - и _.')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', fields['repository']):
        raise ValueError('Репозиторий укажи в формате владелец/репозиторий.')
    catalog_path = root / 'packs/catalog/index.json'
    catalog = None
    if register:
        catalog = json.loads(catalog_path.read_text(encoding='utf-8'))
        if catalog.get('schema') != 1 or not isinstance(catalog.get('packs'), list):
            raise ValueError('Некорректный каталог сборок.')
        if fields['id'] not in catalog['packs']:
            catalog['packs'].append(fields['id'])
    output = root / 'packs' / (fields['id'] + '.json')
    result = build(source, output, fields['id'], fields['name'], fields['version'],
                   fields['minecraft'], fields['forge'], fields['installed_version'],
                   int(fields['java']), fields['repository'], source.relative_to(downloads).as_posix())
    if catalog is not None:
        try:
            atomic_json(catalog_path, catalog)
        except OSError as exc:
            raise OSError(f'Манифест сохранён: {output}, но каталог не обновлён: {exc}') from exc
    return output, result


class PackBuilder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('JFCRAFT — создание сборки')
        self.geometry('820x730')
        self.minsize(760, 690)
        self.busy = False
        self.events = queue.Queue()
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.option_add('*Font', 'SegoeUI 10')
        frame = ttk.Frame(self, padding=24)
        frame.pack(fill='both', expand=True)
        frame.columnconfigure(1, weight=1)
        ttk.Label(frame, text='Создать или обновить сборку', font=('Segoe UI', 18, 'bold')).grid(
            row=0, column=0, columnspan=3, sticky='w', pady=(0, 8))
        ttk.Label(frame, text='Выбери файлы, заполни параметры и сохрани манифест.').grid(
            row=1, column=0, columnspan=3, sticky='w', pady=(0, 16))
        ttk.Button(frame, text='Заполнить из существующего манифеста…', command=self.load).grid(
            row=2, column=0, columnspan=3, sticky='w', pady=(0, 12))
        self.source = tk.StringVar()
        ttk.Label(frame, text='Папка сборки').grid(row=3, column=0, sticky='w')
        ttk.Entry(frame, textvariable=self.source).grid(row=3, column=1, sticky='ew', padx=10)
        ttk.Button(frame, text='Выбрать…', command=self.choose).grid(row=3, column=2)
        ttk.Label(frame, text='Внутри download-files: mods, config, shaderpacks, resourcepacks;\n'
                  'options.txt и servers.dat — в корне. Шейдеры и ресурспаки оставляй ZIP.').grid(
            row=4, column=0, columnspan=3, sticky='w', pady=(6, 14))
        defaults = {'id': '', 'name': '', 'version': '1.0.0', 'minecraft': '1.7.10',
                    'forge': '1.7.10-10.13.4.1614-1.7.10',
                    'installed_version': '1.7.10-Forge10.13.4.1614-1.7.10',
                    'java': '8', 'repository': 'jamesfimmer/JFCRAFT'}
        labels = ['ID сборки', 'Название в лаунчере', 'Версия сборки', 'Minecraft',
                  'Полная версия Forge', 'ID установленного Forge', 'Версия Java', 'GitHub-репозиторий']
        self.fields = {}
        for row, ((key, value), label) in enumerate(zip(defaults.items(), labels), 5):
            self.fields[key] = tk.StringVar(value=value)
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky='w', pady=5)
            widget = (ttk.Combobox(frame, textvariable=self.fields[key], values=('8', '17', '21', '25'))
                      if key == 'java' else ttk.Entry(frame, textvariable=self.fields[key]))
            widget.grid(row=row, column=1, columnspan=2, sticky='ew', padx=(10, 0))
        ttk.Label(frame, text='Для новой сборки задай новый ID. Для обновления сохрани ID и увеличь версию.\n'
                  'Параметры Minecraft / Forge / Java по умолчанию — как у старой LOTR.').grid(
            row=13, column=0, columnspan=3, sticky='w', pady=12)
        self.register = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text='Добавить сборку в каталог лаунчера', variable=self.register).grid(
            row=14, column=0, columnspan=3, sticky='w')
        self.button = ttk.Button(frame, text='Создать / обновить манифест', command=self.save)
        self.button.grid(row=15, column=0, columnspan=3, sticky='ew', pady=14)
        self.progress = ttk.Progressbar(frame, mode='indeterminate')
        self.progress.grid(row=16, column=0, columnspan=3, sticky='ew')
        self.status = tk.StringVar(value='Файлы не публикуются автоматически. После проверки сделай commit и push.')
        ttk.Label(frame, textvariable=self.status, wraplength=730).grid(
            row=17, column=0, columnspan=3, sticky='w', pady=12)
        self.after(100, self.poll)

    def choose(self):
        if self.busy:
            return
        folder = filedialog.askdirectory(parent=self, initialdir=ROOT / 'download-files', title='Папка сборки внутри download-files')
        if folder:
            self.source.set(folder)

    def load(self):
        if self.busy:
            return
        path = filedialog.askopenfilename(parent=self, initialdir=ROOT / 'packs', filetypes=[('Манифест', '*.json')])
        if not path:
            return
        try:
            data = load_manifest(path)
            for key in self.fields:
                if key in data:
                    self.fields[key].set(str(data[key]))
            self.source.set('')
            url = urlsplit(data.get('update_url', ''))
            if url.hostname == 'raw.githubusercontent.com':
                self.fields['repository'].set('/'.join(url.path.strip('/').split('/')[:2]))
            for item in data['files']:
                url_path = unquote(urlsplit(item['url']).path)
                if '/download-files/' in url_path and url_path.endswith('/' + item['path']):
                    folder = url_path.split('/download-files/', 1)[1][:-len(item['path'])].rstrip('/')
                    candidate = (ROOT / 'download-files' / folder).resolve()
                    if candidate.is_relative_to((ROOT / 'download-files').resolve()):
                        self.source.set(str(candidate))
                    break
            self.status.set('Параметры загружены. Для отдельной новой сборки измени ID, название и папку.')
        except Exception as exc:
            messagebox.showerror('Не удалось прочитать манифест', str(exc), parent=self)

    def save(self):
        if self.busy:
            return
        fields = {key: value.get().strip() for key, value in self.fields.items()}
        source = self.source.get().strip()
        if not source or any(not value for value in fields.values()):
            messagebox.showerror('Заполни параметры', 'Выбери папку и заполни все поля.', parent=self)
            return
        if re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}', fields['id']):
            target = ROOT / 'packs' / (fields['id'] + '.json')
            if target.exists() and not messagebox.askyesno('Обновить сборку?',
                    f'Заменить {target.name} описанием текущих файлов?\nДля обновления у игроков увеличь версию сборки.', parent=self):
                return
        register = self.register.get()
        self.busy = True
        self.button.state(['disabled'])
        self.progress.start()
        self.status.set('Считаю контрольные суммы и создаю манифест…')

        def work():
            try:
                output, result = create_pack(ROOT, source, fields, register)
                self.events.put((True, f"Готово: {output}\n{len(result['files'])} файлов, "
                                 f"{sum(item['size'] for item in result['files']) / 1024**2:.1f} МБ. "
                                 + ('Каталог обновлён. ' if register else '')
                                 + 'Проверь сборку и опубликуй файлы, манифест и каталог одним commit/push.'))
            except Exception as exc:
                self.events.put((False, str(exc)))
        threading.Thread(target=work, daemon=True).start()

    def poll(self):
        try:
            success, message = self.events.get_nowait()
        except queue.Empty:
            pass
        else:
            self.busy = False
            self.progress.stop()
            self.button.state(['!disabled'])
            self.status.set(message)
            if not success:
                messagebox.showerror('Не удалось создать сборку', message, parent=self)
        self.after(100, self.poll)

    def close(self):
        if self.busy:
            messagebox.showinfo('Создание сборки', 'Дождись завершения записи манифеста.', parent=self)
        else:
            self.destroy()


if __name__ == '__main__':
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass
    PackBuilder().mainloop()
