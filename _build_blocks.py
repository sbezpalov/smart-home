# -*- coding: utf-8 -*-
import pathlib

mid = pathlib.Path("_mid.txt").read_text(encoding="utf-8").rstrip()
if mid.endswith("---"):
    mid = mid[:-3].rstrip()

pages = """### Подстраницы (черновики, RU)

Сопоставление «в лоб» не всегда верно: **Гостиная** может покрывать **Living Room L/C/F**; **Спальня** в EN-таблице пока не вынесена — добавить строку при инвентаризации.

<page url="https://www.notion.so/35e50b4d730481b4b680f5541b05fc2f">Гостиная</page>
<page url="https://www.notion.so/35e50b4d7304819583cece0491b86ff3">Кухня</page>
<page url="https://www.notion.so/35e50b4d7304812197aae44a9c889e2c">Спальня</page>
<page url="https://www.notion.so/35e50b4d7304819aad01fce01ec7cc3d">Кабинет</page>
<page url="https://www.notion.so/35e50b4d730481ffb20afcd863aabbe4">Коридор</page>

*Источники: **`05-rooms.md`**, **`sources/CX.conf`**, **`sources/CG.conf`**, **`sources/Ruckus.conf`**, **`03-security.md`**, Notion **WiFi**, **Video and Security**.*"""

out = mid + "\n\n" + pages
pathlib.Path("_block_new.txt").write_text(out, encoding="utf-8")

old = """## Расширенная информация по комнатам
План: сценарии, группы света, датчики, цепи электрощита, ссылки на оборудование со страницы **Устройства**.
## Привязка устройств к комнатам
План: матрица «устройство → зона»; для беспроводного покрытия — колонка «AP» в **WiFi** и описания в `Ruckus.conf`.
---
### Подстраницы (черновики, RU)
*Источник в репозитории: **`05-rooms.md`**.*"""
pathlib.Path("_block_old.txt").write_text(old, encoding="utf-8")
print("old", len(old), "new", len(out))
