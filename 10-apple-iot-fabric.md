# Apple-стек в VLAN 10, mDNS-bridge и обновление Devices

> ✅ **Статус: Notion-часть применена 2026-05-13** напрямую через Notion MCP (см. секцию «Что Cursor должен сделать» в конце файла — она переписана). Этот файл — **запись о принятых изменениях** для зеркалирования в git. Все блоки 1–3 ниже описывают то, что **уже находится в Notion**; повторно применять их **не нужно**.

По итогам smart-home review-сессии **2026-05-12 / 2026-05-13**: зафиксированы в Notion архитектурное решение про Apple-в-IoT (ADR-003), двухслойный mDNS-bridge между VLAN 1 и VLAN 10 (новая подстраница на Network), и обновление инвентаризации **Devices** (расширенная таблица, медиа-кластер, vendor-segregated Zigbee, ворота, датчики).

---

## Блок 1 — Добавить ADR-003 на страницу «Архитектурные решения (ADR)»

На существующей странице **🧭 Архитектурные решения (ADR)** (`35e50b4d-7304-8171-a965-ccf05669e0b2`) после блока **ADR-002** добавить:

---

### ADR-003 / 2026-05-13 — Apple-стек в VLAN 10 (IoT) + двухслойный mDNS-bridge

**Контекст.** Aqara M3 (Pri, Sec) физически живут в **VLAN 10 (IoT, `10.254.10.0/24`)** и работают как **Thread Border Router + Matter Bridge** для всей Aqara-экосистемы. HomePod mini × 2 и Apple TV 4K тоже выступают как Thread BR и должны входить в **тот же Thread fabric**, что и M3 — иначе Apple Home ↔ Aqara через Matter работает фрагментарно (mesh не объединяется через L3-границу VLAN). При этом iPhone'ы семьи и общие ресурсы (NAS, принтеры) сидят в **VLAN 1 (Main, `172.16.122.0/24`)** — между ними и Apple-стеком требуется явная propagation mDNS / Bonjour.

**Решение.** Все Apple-устройства (HomePod mini × 2, Apple TV 4K, Haier Smart TV) подключены к **VLAN 10 (IoT)** — по Wi-Fi через SSID **`RSW-Country-Base`**. Между VLAN 1 ↔ VLAN 10 настроен **двухслойный bridge mDNS / Bonjour**:

- **Слой 1 (L3) — FortiGate Multicast Policy:** две bidirectional rules (`Apple Bonjour (Internal)` и `Apple Bonjour (IoT)`) для UDP 5353 / 224.0.0.251.
- **Слой 2 (L2 over Wi-Fi) — Ruckus Bonjour Gateway:** 27 правил из лимита 32, преимущественно направление `1 → 10` для discovery «iPhone в Main → HomePod / Apple TV в IoT», плюс три обратные правила `10 → 1` (AirPlay / AirTunes / Apple TV) для «iPhone в Main как source AirPlay → HomePod как target».

Подробности — отдельная подстраница **«🔊 mDNS / Bonjour между VLAN 1 и VLAN 10»** на странице Network.

**Последствия.** Apple Home + Aqara образуют единый Thread mesh (функционально работает: общий fabric виден в Apple Home / Aqara Home). AirPlay / HomeKit / AirDrop / Continuity между VLAN 1 и VLAN 10 проходят прозрачно. Архитектура зависит от **двух механизмов одновременно** — FortiGate L3 (mDNS-traffic ~100 MB / сторона по счётчикам) и Ruckus L2 (для надёжности multicast over Wi-Fi). Снятие любого из слоёв молча деградирует Apple-discovery.

**Триггер пересмотра.** Загрузка Ruckus Bonjour Gateway достигла **30 / 32** правил (сейчас 27 / 32, headroom 5) — повод сделать ревизию сервисов перед добавлением 33-го. Также — миграция iPhone-парка в другой VLAN, появление третьего L3-сегмента в Apple-fabric, или замена контроллера Ruckus.

---

## Блок 2 — Создать подстраницу «🔊 mDNS / Bonjour между VLAN 1 и VLAN 10»

Создать **дочернюю страницу** под **🌐 Network** (`35e50b4d-7304-8119-b696-d7dcd233311b`), title **«🔊 mDNS / Bonjour между VLAN 1 и VLAN 10»**, иконка `🔊`. Содержимое:

# mDNS / Bonjour между VLAN 1 и VLAN 10

См. **ADR-003**.

## Принцип

Apple-устройства живут в **VLAN 10 (IoT)** для объединения Thread mesh с Aqara M3. iPhone'ы и общие ресурсы (NAS, принтеры, ChromeCast) — в **VLAN 1 (Main)**. Для прозрачной работы AirPlay / HomeKit / AirDrop / Continuity между сегментами настроена **двухслойная propagation mDNS / Bonjour**.

Два слоя — не дублирование, а взаимодополнение:

- **FortiGate L3** покрывает любой ethernet-трафик и весь VLAN-периметр; универсальный, но multicast поверх Wi-Fi на стороне AP может теряться (rate-limit, конверсия в unicast, `band balancing`).
- **Ruckus Bonjour Gateway L2** работает уже внутри Wi-Fi-сегмента: контроллер сам становится источником re-announce'ов в целевом VLAN, обходя проблему multicast over Wi-Fi.

## Слой 1 — FortiGate Multicast Policy

Два правила (bidirectional), оба ACTIVE, SNAT disabled, logging ALL:

| ID | Name | From | To | Source | Destination | Proto | Action | Bytes (на момент снимка) |
|----|------|------|-----|--------|-------------|-------|--------|--------------------------|
| 1 | `Apple Bonjour (Internal)` | internal (VLAN 1) | IoT (VLAN 10) | `ch-network-v4` | `Bonjour` | 17 (UDP) | ACCEPT | 106.47 MB |
| 2 | `Apple Bonjour (IoT)` | IoT (VLAN 10) | internal (VLAN 1) | `ch-iot-v4` | `Bonjour` | 17 (UDP) | ACCEPT | 104.17 MB |

Address objects:

- `ch-network-v4` — подсеть Main `172.16.122.0/24`
- `ch-iot-v4` — подсеть IoT `10.254.10.0/24`
- `Bonjour` — группа `224.0.0.251` (mDNS), UDP port 5353

Объёмы трафика (~100 MB в каждую сторону) подтверждают, что bridge активно используется, а не «настроен и забыт».

## Слой 2 — Ruckus Bonjour Gateway

Контроллер `ch-bezpalov-int` (см. `02-wifi.md`). Лимит платформы — **32 правила**, использовано **27**.

### Группа A — Ruckus-предустановленные сервисы, направление 1 → 10

Под каждой строкой Ruckus сам матчит несколько mDNS service strings.

| # | Bridge Service | From | To | Что обслуживает |
|---|----------------|------|-----|-----------------|
| 1 | AirDisk | 1 | 10 | Apple NAS / Time Machine over network |
| 2 | AirPrint | 1 | 10 | Печать на сетевые принтеры из IoT |
| 3 | AirPlay | 1 | 10 | iPhone (Main) видит Apple TV / HomePod как target |
| 4 | AirTunes | 1 | 10 | Audio streaming pre-AirPlay-2 |
| 5 | Apple TV | 1 | 10 | Обнаружение приставки из Main |
| 6 | iTunes Remote | 1 | 10 | Управление iTunes / Apple Music из Main |
| 7 | GoogleChromeCast | 1 | 10 | ChromeCast discovery (если используется) |
| 8 | Screen Sharing | 1 | 10 | Доступ к macOS Screen Sharing из Main |
| 9 | iCloud Sync | 1 | 10 | Локальный fast-path для синхронизации |
| 10 | Apple File Sharing | 1 | 10 | AFP discovery |
| 11 | Secure File Sharing | 1 | 10 | SMB / encrypted file sharing discovery |
| 12 | Apple Mobile Devices (All...) | 1 | 10 | Continuity / Handoff / Wi-Fi sync |

### Группа B — Низкоуровневые service strings (RFC 6762), направление 1 → 10

Явный список вместо доверия group-shortcut'ам Ruckus:

| # | Service | From | To | Зачем явно |
|---|---------|------|-----|------------|
| 13 | `_appletv-remote._tcp.` | 1 | 10 | Apple TV remote pairing |
| 14 | `_companion-link._tcp.` | 1 | 10 | Companion device (Watch, HomePod) link |
| 15 | `_homekit._tcp.` | 1 | 10 | HomeKit accessory discovery |
| 16 | `_hap._tcp.` | 1 | 10 | HomeKit Accessory Protocol control plane |
| 17 | `_sleep-proxy._udp.` | 1 | 10 | Apple TV как sleep proxy для AirPods / Watch |
| 18 | `_airdrop._tcp.` | 1 | 10 | AirDrop между iPhone (Main) и Mac / Apple TV (IoT) |
| 19 | `_device-info._tcp.` | 1 | 10 | Метаданные устройств Apple |
| 20 | `_roap._tcp.` | 1 | 10 | Remote Audio Output Protocol |
| 21 | `_airserver._tcp.` | 1 | 10 | AirPlay receiver (третьи стороны) |
| 22 | `_eppc._tcp.` | 1 | 10 | Apple Remote Events (AppleScript over network) |
| 23 | `_apple-mobdev2._tcp.` | 1 | 10 | iTunes / Finder Wi-Fi sync (legacy, но используется) |
| 24 | `_remotepairing._tcp.` | 1 | 10 | Apple TV / HomePod remote pairing |

### Группа C — Обратное направление, 10 → 1

Три самых нагруженных «publish-from-IoT» сервиса. Остальные сервисы работают по схеме «клиент в Main спросил → ответ из IoT идёт unicast», поэтому bridge для них в обратку не нужен.

| # | Service | From | To |
|---|---------|------|-----|
| 25 | AirPlay | 10 | 1 |
| 26 | AirTunes | 10 | 1 |
| 27 | Apple TV | 10 | 1 |

### История удалённых правил

| Service | Причина удаления |
|---------|------------------|
| iTunes Sharing | Дублировал `_home-sharing._tcp.`; iTunes media library не используется |
| AirPort Management | В сети нет AirPort base station / Time Capsule (Wi-Fi на Ruckus) |
| `_home-sharing._tcp.` | Дублировал iTunes Sharing, разная грануляция |
| `_net-assistant._tcp.` | Apple Remote Desktop — нужен только при админских Mac в Main |
| `_nut._tcp.` | Network UPS Tools — не относится к Apple Bonjour, наследие |

---

## Блок 3 — Обновить страницу 📱 Устройства

На странице **Устройства** (`35e50b4d-7304-81cc-bf81-cdff3889dcad`):

### 3.1. Заменить основную таблицу инвентаризации новой версией

Новые колонки: **VLAN**, **IP**, **Контур (vendor)**, **Роль**. Содержимое:

| Имя | Модель | Зона (EN) | VLAN | IP | Контур | Роль |
|-----|--------|-----------|------|-----|--------|------|
| Aqara Hub M3 Pri | M3 | Boiler Room | 10 (IoT) | *(уточнить, лучше DHCP-reserve)* | Aqara | Zigbee coordinator + Thread BR + Matter Bridge |
| Aqara Hub M3 Sec | M3 | Kitchen | 10 (IoT) | *(уточнить)* | Aqara | Zigbee coordinator + Thread BR + Matter Bridge |
| Aqara Hub M1S | M1S | Bathhouse | 10 (IoT) | *(уточнить)* | Aqara | Zigbee coordinator (legacy) |
| Camera G2H | G2H | Bathhouse | 10 (IoT) | *(уточнить)* | Aqara | Zigbee hub + камера |
| Air-Conditioner | AR18BSFCMWKNER | Kitchen | 10 (IoT) | *(уточнить)* | Samsung (SmartThings RU) | Кондиционер, ~18000 BTU, WindFree |
| Котёл Kiturami | World Alpha C | Boiler Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Tuya (**NCTR-100WR**, Wi‑Fi) | Газовый котёл; управление через приложение Tuya |
| Apple TV 4K (3 gen) | MN893LL/A | Dining Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Apple | Streamer + **Home Hub** + AirPlay source для HomePod |
| HomePod mini #1 | MJ2D3LL/A | Dining Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Apple | **Stereo pair L** + Thread BR; audio out Apple TV |
| HomePod mini #2 | MY5G2ZP/A | Dining Room | 10 (IoT) | *(уточнить, DHCP-reserve)* | Apple | **Stereo pair R** + Thread BR; audio out Apple TV |
| Haier 50 Smart TV S2 Pro | *(уточнить P/N)* | Dining Room | *(уточнить — см. TODO)* | *(уточнить)* | Haier | Display; вход HDMI от Apple TV 4K |
| YandexStationMini | — | Living Room C | *(уточнить)* | *(уточнить)* | Яндекс (Алиса) | Voice assistant |
| Yandex-Lite-gen2 | — | Living Room L | *(уточнить)* | *(уточнить)* | Яндекс (Алиса) | Voice assistant |

### 3.2. Добавить под таблицей блок про медиа-кластер в Dining Room

> **🎬 Медиа-кластер (Dining Room).** Apple TV 4K является источником видео для **Haier 50 Smart TV S2 Pro** (HDMI) и источником звука для пары **HomePod mini** через AirPlay 2 (стерео-пара, настроена как default audio out для Apple TV). Apple TV одновременно выполняет роль **Home Hub** для Apple Home — это центральная точка отказа в медиа-цепочке и в smart-home-управлении домом.

### 3.3. Переименовать строку Wiren Board

В блоке «Wiren Board → Система»:

- **Было:** «Версия контроллера 8.5.2»
- **Стало:** «Версия ПО (wb-release) 8.5.2 (релиз wb-2602, тип stable)»

Это снимает ложное впечатление, что 8.5.2 — hardware revision. Аппаратная партия указана отдельной строкой «Номер партии: 8.5.2D/4G 1.3.3C-4G» (WB6 + 4G-модуль).

### 3.4. Дополнить блок про WB-Zigbee пояснением vendor-segregation

Под секцией «Wiren Board → Модули расширения» добавить:

> **🧭 Принцип vendor-segregated Zigbee.** В системе сознательно держится **по одному Zigbee-координатору на вендора** — это позволяет избежать неоднородной mesh с Tuya-кластерами, где у вендора часто нестандартная реализация. Распределение:
>
> | Координатор | Контур | Где физически | Назначение |
> |---|---|---|---|
> | Aqara M3 Pri | Aqara | Boiler Room | основные сценарии Aqara |
> | Aqara M3 Sec | Aqara | Kitchen | вторая зона + резервирование |
> | Aqara M1S | Aqara | Bathhouse | банный сегмент (legacy) |
> | Camera G2H | Aqara | Bathhouse | банный сегмент (камера-как-хаб) |
> | Wiren Board `WBE2R-R-ZIGBEE` | Tuya | Boiler Room | пульт Tuya; котёл **Kiturami World Alpha C** (модуль **NCTR-100WR**, Wi‑Fi, **Tuya**); тёплый пол и HA — через Tuya и/или WB-Zigbee *(уточнить канал приоритета)* |
>
> Стек ПО на WB-Zigbee: *(уточнить — `wb-zigbee2mqtt` / стандартный `zigbee2mqtt` / другое)*.
>
> Канал и Pan ID на каждом координаторе — см. TODO ниже (общая Zigbee-таблица каналов).

### 3.5. Добавить недостающие устройства

Добавить новые секции / строки на странице Devices (точное расположение — после основной инвентаризационной таблицы):

#### 🚪 Ворота (Cabin)

| Имя | Модель | Зона (EN) | VLAN | Контур | Роль |
|-----|--------|-----------|------|--------|------|
| Привод ворот Nice | Robo 600 KCE | Cabin | — | Nice | Электропривод откатных ворот |
| Контроллер привода | R0A41 | Cabin | — | Nice | Управляющая плата привода |
| Aqara Dual Relay Module | T2 | Cabin | 10 (IoT) | Aqara | Сухой контакт, импульс на привод |
| Hikvision Single Relay Module | DS-PM1-O1L-WE | Cabin | 50 (Video) | Hikvision | Сухой контакт, импульс на привод |

Управление параллельно от пульта Nice / Aqara T2 / Hikvision AX Pro (сценарии). Привязки и сценарии — `08-ecosystem.md`.

#### 🔥 Безопасность (датчики)

| Имя | Модель / Источник | Зона | Контур | Назначение |
|-----|--------------------|------|--------|------------|
| Датчики дыма | JY-GZ-03AQ | Все жилые комнаты + Bathhouse на каждом этаже | Aqara | Пожарная сигнализация |
| Датчик газа | JT-BZ-03 AQ/A | Boiler Room | Aqara | Утечка газа |
| Hikvision AX Pro | DS-PWA96-M-WE(RU) | Boiler Room | 50 (Video) | Охранная панель, сценарии ворот |

Hikvision AX Pro дублируется в `📹 Video and Security` — здесь только как ссылка на роль в сценариях.

---

## Блок 4 — Открытые TODO, не закрываемые этим патчем

Перечислены, чтобы не потерять.

### Smart-home / IoT (приоритет P0–P1)

- **Zigbee-каналы и Pan ID** для всех 5 координаторов (M3 Pri, M3 Sec, M1S, G2H, WB-Zigbee). Без этой таблицы дальнейшее troubleshooting mesh — угадайка. Рекомендуемая разводка с разносом ≥5 каналов между ближайшими координаторами и с разносом от Wi-Fi-каналов Ruckus.
- **Стек ПО на WB-Zigbee** — `wb-zigbee2mqtt` / стандартный `zigbee2mqtt` / ZHA / Deconz.
- **Котёл Kiturami** — зафиксировано: **Kiturami World Alpha C**, модуль **NCTR-100WR** (Wi‑Fi, Tuya). Остаётся: DHCP-reserve / VLAN учёт для модуля, интеграция в HA (Tuya vs WB-Zigbee для тёплого пола), SLA/runbook при отказе облака Tuya или пути через WB (**ADR-002** — бэкап WB).
- **Haier 50 Smart TV S2 Pro** — три параметра: (1) на каком VLAN сидит; (2) HDMI-CEC включён? (3) Smart-функции Haier — оставлены или выключены (Wi-Fi отключён) в пользу Apple TV? Best practice — отключить Smart-функции Haier, чтобы убрать вендорскую телеметрию.
- **DHCP-резервации** для HomePod mini × 2 и Apple TV 4K на FortiGate (стабильные IP для отладки mDNS, Zabbix-мониторинга, фильтрации).
- **Mosquitto auth + ACL** на брокере `10.254.10.2:1883` — добавить `mosquitto.passwd` и разделить топики `homeassistant/#`, `wb-rules/#`, `lavritech/#` под отдельных пользователей.
- **Двойной хаб в Bathhouse (G2H + M1S)** — решить: консолидировать на одном (предпочтительно G2H) или явно описать роли. Сейчас оба на близких Zigbee-каналах — риск интерференции.

### Voice / голосовые контуры

- **Матрица voice fabric** на странице **Настройки и интеграции**: `устройство × Алиса × Сири × кто primary`. Сейчас Yandex и Apple Home — два конкурирующих контура без архитектурного решения «кто primary для управления чем».

### Документация и changelog

- **Чистка устаревших ADR-ссылок в `03-security.md` / Notion Video and Security.** После консолидации журнала ADR (теперь только ADR-001 и ADR-002) ссылки в callout «Стратегия архива: Hik-Cloud (**ADR-002**) … D6/D7 — accepted exception (**ADR-003**)» — **протухли**: ADR-002 в актуальной нумерации это «бэкап конфигов», а ADR-003 — это новый mDNS-bridge из текущего патча. Варианты починки (на выбор):
  - **A — переформулировать callout без номеров ADR**: оставить только операционные факты («архив — Hik-Cloud», «D6/D7 — accepted exception, временные») без ссылок на несуществующие ADR-NNN. Самый чистый путь, согласован с решением «эти темы не на уровне ADR».
  - **B — восстановить ADR**: добавить ADR-004 (Hik-Cloud strategy) и ADR-005 (D6/D7 temporary cameras) в журнал. Менять в моём патче нумерацию mDNS-ADR (он будет ADR-006 вместо ADR-003).
  - Рекомендация — **вариант A**.
- **Запустить changelog** в `📅 История изменений`. Первая запись: «2026-05-12 — замена deprecated моделей OpenAI в 3CX AI Agents (`gpt-realtime` → `gpt-realtime-1.5`, `gpt-4o` → `gpt-5.4-mini`)».
- **Подстраницы автоматизаций** (Освещение / Климат / Безопасность / Медиа) — все ещё пусты. Хотя бы один работающий сценарий в каждой задаст шаблон.
- **Связь Devices ↔ Rooms** — колонки `Освещение / Климат / Безопасность / Медиа` на странице Rooms можно дозаполнить из обновлённой инвентаризации Devices.

### Сохранилось с прошлой сессии

- Bridge HQ на странице Voice — описать удалённую площадку, тип туннеля, BCDR.
- D8 (`10.0.50.5`) — задокументировать подсеть или нормализовать.
- Зоны камер D1–D9 на Notion-странице Rooms / Video and Security.
- Конфиг Dahua DH-CS4006-4GT-60 в `sources/`.
- Идентификация трёх DNS (`172.16.122.254`, `172.16.121.254`, `172.16.120.2`).
- Toll-fraud-лимиты в 3CX (`International / 810`, лимиты длительности + суточные).

---

## Что Cursor должен сделать по этому файлу

> ⚠️ **Важно: Notion уже синхронизирован.** Блоки 1–3 этого файла применены в Notion напрямую (`2026-05-13`, через Notion MCP в чате). Cursor **не должен** повторно применять их через свой Notion MCP — это создаст дубликаты страницы mDNS, дубль ADR-003 и дубль блоков на Devices.

Cursor нужно только:

1. **Положить** этот файл в репозиторий как `10-apple-iot-fabric.md` (если его там ещё нет).
2. **Закоммитить** сообщением:
   ```
   docs: ADR-003 + mDNS bridge VLAN1↔VLAN10 + Devices update (Apple media cluster, vendor-segregated Zigbee)
   ```
3. **Не коммитить** содержимое `sources/*.conf`.
4. **Опционально:** добавить первую запись в Notion `📅 История изменений` — «2026-05-13 — ADR-003, mDNS-bridge документация, обновление Devices: Apple media cluster, vendor-segregated Zigbee, недостающие устройства (ворота, датчики)». Этот раздел Notion пока пуст, и эта запись станет первой.

Если потребуется внести правки в материалы блоков 1–3 — править надо **в Notion как source of truth**, затем синхронизировать обратно в этот файл (по той же модели, что и другие `0X-*.md`).
