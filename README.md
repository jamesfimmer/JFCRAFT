# JFCRAFT

Лаунчер Minecraft-сборок для Windows: Vanilla Expanded, Pokecraft, New IC,
Winter Craft и Middle-earth Chronicles Classic.

Скачай `JFCRAFT.exe` из [Releases](https://github.com/jamesfimmer/JFCRAFT/releases),
выбери ник, память и Java, затем нажми **Играть**. Первая установка скачивает
Minecraft, Forge и файлы сборки. Для обслуживания используй меню **⋯**:

- **Обновить / восстановить** — обновить описание и файлы;
- **Открыть папку сборки** — открыть профиль;
- **Удалить сборку** — сохранить весь профиль, включая миры, в резервной папке.

Лишние моды удаляются в резервную копию, миры в `saves` не изменяются. Шейдеры и
ресурспаки устанавливаются готовыми ZIP-файлами в `shaderpacks` и `resourcepacks`.
Для LOTR нужна Java 8, для современных сборок — Java 17. Вход Microsoft пока не подключён.

Данные находятся в `%APPDATA%/JFCRAFT/instances`.

## Разработка

```powershell
python -m pip install -r requirements.txt
python main.py
python -m unittest discover -s tests
python tools/audit_catalog.py
```

Манифесты — в `packs`, каталог — `packs/catalog/index.json`. EXE собирается командой
`python build_exe.py`; готовый файл появится в `dist/JFCRAFT.exe`.
