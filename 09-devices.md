> **Синхронизация:** Notion **[Устройства](https://www.notion.so/35e50b4d730481ccbf81cdff3889dcad)** — первичный источник (импорт **2026-05-15**). Этот файл — зеркало; при расхождении правьте Notion, затем подтяните сюда. Wiren Board / LoRaWAN — [`07-wirenboard.md`](07-wirenboard.md).

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
| Doorbell G4 | G4 | Крыльцо | Doorstep |

Экосистемы и протоколы — ниже и в [`08-ecosystem.md`](08-ecosystem.md).

---

## Расширенная инвентаризация (VLAN / IP / контур / роль)

Связано с **ADR-003** (Apple-стек в VLAN 10 + mDNS-bridge). IP — *(уточнить и сделать DHCP-reserve)*.

| Имя | Модель | Зона (EN) | VLAN | IP | Контур | Роль |
|-----|--------|-----------|------|-----|--------|------|
| Aqara Hub M3 Pri | M3 | Boiler Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Aqara | Zigbee coordinator + Thread BR + Matter Bridge |
| Aqara Hub M3 Sec | M3 | Kitchen | 10 (IoT) | *(уточнить, DHCP-reserve)* | Aqara | Zigbee coordinator + Thread BR + Matter Bridge |
| Aqara Hub M1S | M1S | Bathhouse | 10 (IoT) | *(уточнить, DHCP-reserve)* | Aqara | **Zigbee coordinator бани** (`54EF44322EBA`) |
| Camera G2H | G2H | Bathhouse | 10 (IoT) | *(уточнить, DHCP-reserve)* | Aqara | Камера; **самостоятельный** hub (`lumi1.54ef44350ea7`) |
| Air-Conditioner | AR18BSFCMWKNER | Kitchen | 10 (IoT) | *(уточнить, DHCP-reserve)* | Samsung (SmartThings RU) | Кондиционер, ~18000 BTU, WindFree |
| Apple TV 4K (3 gen) | MN893LL/A | Dining Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Apple | Streamer + **Home Hub** · AirPlay source для HomePod |
| HomePod mini #1 | MJ2D3LL/A | Dining Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Apple | **Stereo pair L** · Thread BR; audio out Apple TV |
| HomePod mini #2 | MY5G2ZP/A | Dining Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Apple | **Stereo pair R** · Thread BR; audio out Apple TV |
| Haier 50 Smart TV S2 Pro | *(уточнить P/N)* | Dining Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Haier | Display; вход HDMI от Apple TV 4K |
| YandexStationMini | — | Living Room C | 10 (IoT) | *(уточнить, DHCP-reserve)* | Яндекс (Алиса) | Voice assistant |
| Yandex-Lite-gen2 | — | Living Room L | 10 (IoT) | *(уточнить, DHCP-reserve)* | Яндекс (Алиса) | Voice assistant |
| Котёл Kiturami | World Alpha C | Boiler Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Tuya (модуль **NCTR-100WR**, Wi‑Fi) | Газовый котёл |
| Doorbell G4 | Aqara Doorbell Camera Hub **G4** | Doorstep | 10 (IoT) | *(уточнить, DHCP-reserve)* | Aqara | Видеозвонок на **крыльце**; **динамик (chime)** в **Living Room F** · `lumi1.54ef445d9665` |

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

Зона участка — **Bathhouse**; в **Aqara Home** комната может называться *Bathroom*. VLAN **10 (IoT)**; Wi‑Fi — **ch-ext-ap**.

> **Распределение хабов:** вся периферия Aqara в бане (1F и 2F) — координатор **Hub M1S** (`54EF44322EBA`). Исключение — **Camera G2H** (`lumi1.54ef44350ea7`): самостоятельный hub (камера), периферию бани не обслуживает.

### Bathhouse 1F

| Имя (UI) | Модель | Device ID | Назначение / привязки |
|----------|--------|-----------|------------------------|
| Hub M1S | Aqara Hub M1S | `54EF44322EBA` | **Координатор бани**; встроенная лампа (ночник) |
| Camera G2H | Aqara Camera Hub G2H | `lumi1.54ef44350ea7` | Камера; **отдельный** hub (не координатор периферии) |
| Dual control module | Aqara Dual control module | `158D008B85FCC5` | **Switch 1** — фонарь на улице; **Switch 2** — освещение в предбаннике |
| Motion Sensor | Aqara Motion Sensor | `158D00075FA343` | Движение |
| Remote Switch | Aqara Wireless Remote Switch H1 (Double Rocker) | `54EF441000EB56DC` | Управляет реле `158D008B85FCC5` |
| Smoke Detector | Aqara JY-GZ-03AQ | `54EF441000809CAE` | Пожарный датчик дыма |
| Temperature and Humidity Sensor | Aqara Temperature and Humidity Sensor | `158D0008DFC108` | Климат |

### Bathhouse 2F

| Имя (UI) | Модель | Device ID | Назначение |
|----------|--------|-----------|------------|
| Smoke Detector | Aqara JY-GZ-03AQ | `54EF44100080A1A1` | Пожарный датчик дыма |

Сводка по зонам — [`05-rooms.md`](05-rooms.md).

---

## Крыльцо (Doorstep) — Aqara

Зона **Doorstep** (план **10**); в **Aqara Home** комната звонка — *Doorstep* / крыльцо. VLAN **10 (IoT)**. Параллельно с Hikvision **DS-KV6113** (калитка, VLAN 50) — другой контур.

| Имя (UI) | Модель | Device ID | Зона установки | Роль |
|----------|--------|-----------|----------------|------|
| Doorbell G4 | Aqara Doorbell Camera Hub **G4** | `lumi1.54ef445d9665` | **Doorstep** (кнопка / камера на крыльце) | Видеозвонок, детекция у двери |
| *(динамик G4)* | *(в составе G4)* | `lumi1.54ef445d9665` | **Living Room F** | Звонок внутри дома (chime) |

> Один аксессуий **G4**: наружный блок на **Doorstep**, внутренний динамик привязан к комнате **Living Room F** в Aqara Home / Apple Home.

---

## Ворота (Cabin)

| Имя (UI) | Модель | Device ID | Зона (EN) | VLAN | Контур | Роль |
|----------|--------|-----------|-----------|------|--------|------|
| Привод ворот Nice | Robo 600 KCE | | Cabin | — | Nice | Электропривод откатных ворот |
| Контроллер привода | R0A41 | | Cabin | — | Nice | Управляющая плата привода |
| Dual Relay Module | Aqara Dual Relay Module T2 | `54EF441000CEB880` | Cabin | 10 (IoT) | Aqara | Сухой контакт, импульс на привод 300ms |
| Single Relay Module | Hikvision DS-PM1-O1L-WE | | Cabin | 50 (Video) | Hikvision | Сухой контакт, импульс на привод |

Управление параллельно от пульта Nice / Aqara T2 / Hikvision AX Pro (сценарии). Привязки — [`08-ecosystem.md`](08-ecosystem.md).

---

## Безопасность (датчики)

| Имя (UI) | Модель | Зона | Контур | Назначение |
|----------|--------|------|--------|------------|
| Датчик дыма | JY-GZ-03AQ | Все жилые комнаты + Bathhouse на каждом этаже | Aqara | Пожарная сигнализация |
| Датчик газа | JT-BZ-03 AQ/A | Boiler Room | Aqara | Утечка газа |
| Hikvision AX Pro | DS-PWA96-M-WE(RU) | Boiler Room | 50 (Video) | Охранная панель, сценарии ворот |

Hikvision AX Pro дублируется в [`03-security.md`](03-security.md) — здесь только роль в сценариях.

---

## Связанные разделы

- [`08-ecosystem.md`](08-ecosystem.md) — роли Aqara M3, SmartThings, Apple Home, HA.
- [`05-rooms.md`](05-rooms.md) — зоны и план помещений.
- [`02-wifi.md`](02-wifi.md) — SSID и покрытие AP.
- [`01-network.md`](01-network.md) — VLAN 10, mDNS / Bonjour.
- [`10-apple-iot-fabric.md`](10-apple-iot-fabric.md) — ADR-003 и таблицы mDNS (git-зеркало).
