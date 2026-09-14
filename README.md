# JFCRAFT

Лаунчер Minecraft-сборок для Windows: Vanilla Expanded, Pokecraft, New IC,
Winter Craft и Middle-earth Chronicles Classic.

Скачай `JFCRAFT.exe` из [Releases](https://github.com/jamesfimmer/JFCRAFT/releases),
выбери ник, память и Java, затем нажми **Играть**. Первая установка скачивает
Minecraft, Forge и файлы сборки. «Играть» проверяет обновления и исправляет файлы
перед запуском. При недоступности сети запускается уже установленный выпуск;
для первой установки нужен интернет. Для обслуживания используй меню **⋯**:

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
python tools/audit_catalog.py --working-tree
```

Манифесты — в `packs`, каталог — `packs/catalog/index.json`. Файлы лежат отдельно
в `download-files/<folder>/mods`, `config`, `shaderpacks`, `resourcepacks`;
внешние RAR/ZIP-контейнеры не нужны. Для новой сборки выполни:

```powershell
python tools/build_pack.py download-files/MyPack packs/my-pack.json --folder MyPack --id my-pack --name "My Pack" --version 1.0.0 --minecraft 1.20.1 --forge 1.20.1-47.3.0 --installed-version 1.20.1-forge-47.3.0 --java 17
```

Добавь ID в каталог. Публикуй файлы и манифесты одним commit/push. Ссылки указывают
на `main`, а контрольные суммы защищают от несовпадения содержимого. Releases используются только
для распространения `JFCRAFT.exe`. EXE собирается командой `python build_exe.py`.

Свой логотип для EXE положи в `assets/jfcraft-logo.png`; следующая сборка подхватит его автоматически.
