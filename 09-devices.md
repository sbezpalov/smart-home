# Устройства (инвентаризация)

Площадка **`ch-`** (country house) — см. префиксы и сети в [`01-network.md`](01-network.md). Ниже — первый снимок учёта; скриншот таблицы: [`assets/devices-inventory-ch.png`](assets/devices-inventory-ch.png).

Полная база в Notion — **[Устройства](https://www.notion.so/35e50b4d730481ccbf81cdff3889dcad)**. Дальше удобно вести поля: тип, производитель, комната, протокол, IP/hostname, статус.

---

## Контур Aqara, климат, медиа (начальный список)

| Имя (учёт) | Модель / P/N | Зона (RU) | Зона (док) | Экосистема / протокол | Примечание |
|------------|--------------|-----------|------------|------------------------|------------|
| **Aqara Hub M3 Pri** | **M3** | Бойлерная | **Boiler Room** | Zigbee, Matter, Thread (Aqara) | Основной хаб участка; см. [`08-ecosystem.md`](08-ecosystem.md) |
| **Aqara Hub M1S** | **M1S** | Баня | **Bathhouse** | Zigbee (Aqara) | Второй хаб на бане |
| **Camera G2H** | **G2H** | Баня | **Bathhouse** | Aqara (камера + Zigbee hub в линейке G2H) | Уточнить режим Zigbee относительно **M1S** на той же зоне |
| **Aqara Hub M3 Sec** | **M3** | Кухня | **Kitchen** | Zigbee, Matter, Thread (Aqara) | Второй **M3** в доме (кухня) |
| **Air-Conditioner** | **AR18BSFCMWKNER** | Кухня | **Kitchen** | Wi‑Fi (Samsung SmartThings) | По [`08-ecosystem.md`](08-ecosystem.md) — **SmartThings только для кондиционера** |
| **YandexStationMini** | — | Спальня C | **Living Room C** | Wi‑Fi (Яндекс) | См. нумерацию плана в [`05-rooms.md`](05-rooms.md) |
| **Yandex-Lite-gen2** | — | Спальня L | **Living Room L** | Wi‑Fi (Яндекс) | |
| **TV 4K** | **MN893LL/A** | Гостиная | **Dining Room** (план **09**, «гостиная» в чертеже) | Wi‑Fi / Ethernet; экосистема Apple TV | Модель соответствует **Apple TV 4K** |
| **HomePod Mini** | **MJ2D3LL/A** | Гостиная | **Dining Room** | Wi‑Fi, Thread (Apple Home) | |
| **HomePod Mini** | **MY5G2ZP/A** | Гостиная | **Dining Room** | Wi‑Fi, Thread (Apple Home) | Второй экземпляр (другая модель/регион) |

---

## Связанные разделы

- [`08-ecosystem.md`](08-ecosystem.md) — роли Aqara M3, SmartThings, Apple Home, HA.
- [`05-rooms.md`](05-rooms.md) — зоны и план помещений.
- [`02-wifi.md`](02-wifi.md) — SSID и покрытие AP.
