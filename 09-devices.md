> **Синхронизация:** выровнено с Notion **[Устройства](https://www.notion.so/35e50b4d730481ccbf81cdff3889dcad)** (первичный источник; импорт **2026-05-14**). Детали Wiren Board, LoRaWAN, Zigbee-контуров — [`07-wirenboard.md`](07-wirenboard.md).

# Устройства (инвентаризация)

Площадка **`ch-`** (country house) — см. префиксы и сети в [`01-network.md`](01-network.md). Скриншот первой таблицы: [`assets/devices-inventory-ch.png`](assets/devices-inventory-ch.png).

---

## Инвентаризация (ch-, первая выгрузка)

| Имя | Модель | Зона (RU) | Зона (EN) |
|-----|--------|-----------|-----------|
| Aqara Hub M3 Pri | M3 | Бойлерная | Boiler Room |
| Aqara Hub M1S | M1S | Баня | Bathhouse |
| Camera G2H | G2H | Баня | Bathhouse |
| Aqara Hub M3 Sec | M3 | Кухня | Kitchen |
| Air-Conditioner | AR18BSFCMWKNER | Кухня | Kitchen |
| YandexStationMini | — | Спальня C | Living Room C |
| Yandex-Lite-gen2 | — | Спальня L | Living Room L |
| TV 4K | MN893LL/A | Гостиная | Dining Room |
| HomePod Mini | MJ2D3LL/A | Гостиная | Dining Room |
| HomePod Mini | MY5G2ZP/A | Гостиная | Dining Room |

Экосистемы и протоколы — ниже и в [`08-ecosystem.md`](08-ecosystem.md).

---

## Расширенная инвентаризация (VLAN / IP / контур / роль)

Связано с **ADR-003** (Apple-стек в VLAN 10 + mDNS-bridge). IP — *(уточнить и сделать DHCP-reserve)*.

| Имя | Модель | Зона (EN) | VLAN | IP | Контур | Роль |
|-----|--------|-----------|------|-----|--------|------|
| Aqara Hub M3 Pri | M3 | Boiler Room | 10 (IoT) | *(уточнить)* | Aqara | Zigbee coordinator + Thread BR + Matter Bridge |
| Aqara Hub M3 Sec | M3 | Kitchen | 10 (IoT) | *(уточнить)* | Aqara | Zigbee coordinator + Thread BR + Matter Bridge |
| Aqara Hub M1S | M1S | Bathhouse | 10 (IoT) | *(уточнить)* | Aqara | Zigbee coordinator (legacy) |
| Camera G2H | G2H | Bathhouse | 10 (IoT) | *(уточнить)* | Aqara | Zigbee hub + камера |
| Air-Conditioner | AR18BSFCMWKNER | Kitchen | 10 (IoT) | *(уточнить)* | Samsung (SmartThings RU) | Кондиционер, ~18000 BTU, WindFree |
| Apple TV 4K (3 gen) | MN893LL/A | Dining Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Apple | Streamer + **Home Hub** · AirPlay source для HomePod |
| HomePod mini #1 | MJ2D3LL/A | Dining Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Apple | **Stereo pair L** · Thread BR; audio out Apple TV |
| HomePod mini #2 | MY5G2ZP/A | Dining Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Apple | **Stereo pair R** · Thread BR; audio out Apple TV |
| Haier 50 Smart TV S2 Pro | *(уточнить P/N)* | Dining Room | *(уточнить — см. TODO)* | *(уточнить)* | Haier | Display; вход HDMI от Apple TV 4K |
| YandexStationMini | — | Living Room C | *(уточнить)* | *(уточнить)* | Яндекс (Алиса) | Voice assistant |
| Yandex-Lite-gen2 | — | Living Room L | *(уточнить)* | *(уточнить)* | Яндекс (Алиса) | Voice assistant |

### Медиа-кластер (Dining Room)

> Apple TV 4K является источником видео для **Haier 50 Smart TV S2 Pro** (HDMI) и источником звука для пары **HomePod mini** через AirPlay 2 (стерео-пара, настроена как default audio out для Apple TV). Apple TV одновременно выполняет роль **Home Hub** для Apple Home — это центральная точка отказа в медиа-цепочке и в smart-home-управлении домом.

---

## Ворота (Cabin)

| Имя | Модель | Зона (EN) | VLAN | Контур | Роль |
|-----|--------|-----------|------|--------|------|
| Привод ворот Nice | Robo 600 KCE | Cabin | — | Nice | Электропривод откатных ворот |
| Контроллер привода | R0A41 | Cabin | — | Nice | Управляющая плата привода |
| Aqara Dual Relay Module | T2 | Cabin | 10 (IoT) | Aqara | Сухой контакт, импульс на привод |
| Hikvision Single Relay Module | DS-PM1-O1L-WE | Cabin | 50 (Video) | Hikvision | Сухой контакт, импульс на привод |

Управление параллельно от пульта Nice / Aqara T2 / Hikvision AX Pro (сценарии). Привязки — [`08-ecosystem.md`](08-ecosystem.md).

---

## Безопасность (датчики)

| Имя | Модель / источник | Зона | Контур | Назначение |
|-----|-------------------|------|--------|------------|
| Датчики дыма | JY-GZ-03AQ | Все жилые комнаты + Bathhouse на каждом этаже | Aqara | Пожарная сигнализация |
| Датчик газа | JT-BZ-03 AQ/A | Boiler Room | Aqara | Утечка газа |
| Hikvision AX Pro | DS-PWA96-M-WE(RU) | Boiler Room | 50 (Video) | Охранная панель, сценарии ворот |

AX Pro дублируется в Notion **Video and Security** / [`03-security.md`](03-security.md).

---

## Связанные разделы

- [`08-ecosystem.md`](08-ecosystem.md) — роли Aqara M3, SmartThings, Apple Home, HA.
- [`05-rooms.md`](05-rooms.md) — зоны и план помещений.
- [`02-wifi.md`](02-wifi.md) — SSID и покрытие AP.
- [`01-network.md`](01-network.md) — VLAN 10, mDNS / Bonjour.
- [`10-apple-iot-fabric.md`](10-apple-iot-fabric.md) — ADR-003 и таблицы mDNS (git-зеркало).
