# JFCRAFT

Лаунчер Minecraft-сборок для Windows: Vanilla Expanded, Pokecraft, New IC,
Winter Craft и Middle-earth Chronicles Classic.

Скачай `JFCRAFT.exe` из [Releases](https://github.com/jamesfimmer/JFCRAFT/releases),
выбери ник и память, затем нажми **Играть**. Каталог сборок обновляется при открытии в фоне. Java подбирается автоматически; если её нет, лаунчер скачает проверенную Temurin x64. Первая установка скачивает
Minecraft, Forge и файлы сборки. «Играть» проверяет обновления и исправляет файлы
перед запуском. При недоступности сети запускается уже установленный выпуск;
для первой установки нужен интернет. Для обслуживания используй меню **⋯**:

- **Восстановить сборку** — проверить Minecraft, Forge и файлы, докачать отсутствующее или повреждённое;
- **Открыть папку сборки** — открыть профиль;
- **Удалить сборку** — сохранить весь профиль, включая миры, в резервной папке.

Лишние моды удаляются в резервную копию, миры в `saves` не изменяются. Шейдеры и
ресурспаки устанавливаются готовыми ZIP-файлами в `shaderpacks` и `resourcepacks`.
Java хранится в `%APPDATA%/JFCRAFT/runtimes` и повторно используется без интернета. Для новой LOTR также автоматически подбирается Java 21 для перезапуска. Ручной выбор Java доступен в меню **⋯**. Вход Microsoft пока не подключён.

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

Создание сборок через окно: `python build_pack_ui.py`. Выбери папку внутри `download-files`, заполни параметры или загрузи существующий манифест. Окно сохраняет манифест и добавляет ID в каталог; commit/push выполняется вручную. Для новой сборки нужен новый ID, для обновления — новая версия.

Актуальная сборка с сервером задаётся полем `featured` в `packs/catalog/index.json` (ID сборки). Она показывается отдельной карточкой над остальными. `null` отключает выделение.
