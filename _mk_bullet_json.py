# -*- coding: utf-8 -*-
import json
import pathlib

old = """## Расширенная информация по комнатам
План: сценарии, группы света, датчики, цепи электрощита, ссылки на оборудование со страницы **Устройства**.
## Привязка устройств к комнатам
План: матрица «устройство → зона»; для беспроводного покрытия — колонка «AP» в **WiFi** и описания в `Ruckus.conf`.
---
### Подстраницы (черновики, RU)
Временная заглушка: раздел пересобирается."""

new = pathlib.Path("_block_bullets.txt").read_text(encoding="utf-8").strip()
assert "`Ruckus.conf`" in old
pathlib.Path("_bullet_update.json").write_text(
    json.dumps(
        {
            "page_id": "35e50b4d-7304-81d9-8c42-c88fecbe07e1",
            "command": "update_content",
            "properties": {},
            "content_updates": [{"old_str": old, "new_str": new}],
        },
        ensure_ascii=False,
        separators=(",", ":"),
    ),
    encoding="utf-8",
)
print("ok")
