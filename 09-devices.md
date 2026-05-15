> **Синхронизация:** выровнено с Notion **[Устройства](https://www.notion.so/35e50b4d730481ccbf81cdff3889dcad)** (первичный источник; баня Aqara **2026-05-15**). Детали Wiren Board, LoRaWAN, Zigbee-контуров — [`07-wirenboard.md`](07-wirenboard.md).

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
| Котёл Kiturami | World Alpha C | Бойлерная | Boiler Room |
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
| Aqara Hub M1S | M1S | Bathhouse | 10 (IoT) | *(уточнить)* | Aqara | **Zigbee coordinator бани** (`54EF44322EBA`) |
| Camera G2H | G2H | Bathhouse | 10 (IoT) | *(уточнить)* | Aqara | Камера; **самостоятельный** hub (`lumi1.54ef44350ea7`) |
| Air-Conditioner | AR18BSFCMWKNER | Kitchen | 10 (IoT) | *(уточнить)* | Samsung (SmartThings RU) | Кондиционер, ~18000 BTU, WindFree |
| Apple TV 4K (3 gen) | MN893LL/A | Dining Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Apple | Streamer + **Home Hub** · AirPlay source для HomePod |
| HomePod mini #1 | MJ2D3LL/A | Dining Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Apple | **Stereo pair L** · Thread BR; audio out Apple TV |
| HomePod mini #2 | MY5G2ZP/A | Dining Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Apple | **Stereo pair R** · Thread BR; audio out Apple TV |
| Haier 50 Smart TV S2 Pro | *(уточнить P/N)* | Dining Room | *(уточнить — см. TODO)* | *(уточнить)* | Haier | Display; вход HDMI от Apple TV 4K |
| YandexStationMini | — | Living Room C | *(уточнить)* | *(уточнить)* | Яндекс (Алиса) | Voice assistant |
| Yandex-Lite-gen2 | — | Living Room L | *(уточнить)* | *(уточнить)* | Яндекс (Алиса) | Voice assistant |
| Котёл Kiturami | World Alpha C | Boiler Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Tuya (**NCTR-100WR**, Wi‑Fi) | Газовый котёл; штатное управление — приложение **Tuya** |

### Медиа-кластер (Dining Room)

> Apple TV 4K является источником видео для **Haier 50 Smart TV S2 Pro** (HDMI) и источником звука для пары **HomePod mini** через AirPlay 2 (стерео-пара, настроена как default audio out для Apple TV). Apple TV одновременно выполняет роль **Home Hub** для Apple Home — это центральная точка отказа в медиа-цепочке и в smart-home-управлении домом.

### Котёл и отопление (Boiler Room)

| Узел | Модель / модуль | Сеть / контур | Примечание |
|------|-----------------|---------------|------------|
| Газовый котёл | **Kiturami World Alpha C** | — | Установка в **Boiler Room** |
| Управляющий модуль | **NCTR-100WR** | **Wi‑Fi**, экосистема **Tuya** | Основной канал управления/мониторинга котла через приложение Tuya |
| Тёплый пол + WB-Zigbee | см. [`07-wirenboard.md`](07-wirenboard.md) | Tuya (Zigbee координатор на WB) | Связка с HA — через Tuya-интеграции и/или Zigbee на **WBE2R-R-ZIGBEE** *(уточнить приоритет и фактическую схему)* |

---

## Баня (Bathhouse) — контур Aqara

Зона участка — **Bathhouse** (RU: баня); в **Aqara Home** комната может называться *Bathroom*. Сеть: VLAN **10 (IoT)**, покрытие Wi‑Fi — **ch-ext-ap** (outdoor).

**Распределение хабов:** все перечисленные ниже устройства Aqara в бане (1F и 2F) привязаны к координатору **Hub M1S** (`54EF44322EBA`). Исключение — **Camera G2H** (`lumi1.54ef44350ea7`): самостоятельный хаб (камера + свой Zigbee-контур), периферию бани **не** обслуживает.

**Координаторы (хабы):**

| Имя (UI) | Модель | Device ID | Этаж | Роль |
|----------|--------|-----------|------|------|
| Hub M1S | Aqara Hub **M1S** | `54EF44322EBA` | 1F | **Основной Zigbee-координатор бани**; встроенная **лампа (ночник)** |
| Camera G2H | Aqara Camera Hub **G2H** | `lumi1.54ef44350ea7` | 1F | Камера; **отдельный** hub (не координатор для остальной периферии) |

### Bathhouse 1F — периферия Zigbee (координатор **M1S**)

| Имя (UI) | Модель | Device ID | Назначение / привязки |
|----------|--------|-----------|------------------------|
| Dual control module | Aqara **Dual control module** | `158D008B85FCC5` | **Switch 1** — фонарь на улице; **Switch 2** — освещение в предбаннике |
| Motion Sensor | Aqara **Motion Sensor** | `158D00075FA343` | Движение |
| Remote Switch | Aqara **Wireless Remote Switch H1** (Double Rocker) | `54EF441000EB56DC` | Управляет реле **`158D008B85FCC5`** |
| Smoke Detector | Aqara **JY-GZ-03AQ** | `54EF441000809CAE` | Пожарный датчик дыма |
| Temperature and Humidity Sensor | Aqara **Temperature and Humidity Sensor** | `158D0008DFC108` | Климат (температура / влажность) |

### Bathhouse 2F (координатор **M1S**)

| Имя (UI) | Модель | Device ID | Назначение |
|----------|--------|-----------|------------|
| Smoke Detector | Aqara **JY-GZ-03AQ** | `54EF44100080A1A1` | Пожарный датчик дыма |

Сводка по освещению и безопасности бани — также [`05-rooms.md`](05-rooms.md) (матрица IoT по зонам).

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
| Датчики дыма | JY-GZ-03AQ | Все жилые комнаты + **Bathhouse** (1F: `54EF441000809CAE`, 2F: `54EF44100080A1A1`) | Aqara | Пожарная сигнализация |
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
