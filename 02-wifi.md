> **Синхронизация:** выровнено с Notion **[WiFi](https://www.notion.so/35e50b4d7304812092f0d876c1c72728)** (первичный источник). Экспорт контроллера — `sources/Ruckus.conf`.

# Беспроводная сеть

## Точки доступа (AP)

Контроллер **ch-bezpalov-int**; зона **RU, NNOV, Country House**. На всех AP: **802.11ax** на 2.4 и 5 ГГц, **канал и ширина — Auto**, **DFS включён**, **Tx Power — Auto**, WLAN group **System Default**.

| Точка доступа | Имя в ZC / Ruckus | Модель | Расположение (Description) | Канал (2.4 GHz) | Канал (5 GHz) | Мощность |
|---------------|-------------------|--------|---------------------------|-----------------|---------------|----------|
| AP-1 | **ch-int-ap-02** | Ruckus **R550** | Living Room L | Auto | Auto | Auto |
| AP-2 | **ch-int-ap-01** | Ruckus **R550** | Dining Room | Auto | Auto | Auto |
| AP-3 | **ch-int-ap-04** | Ruckus **R350** | Living Room C | Auto | Auto | Auto |
| AP-4 | **ch-int-ap-03** | Ruckus **R350** | Living Room F | Auto | Auto | Auto |
| AP-5 | **ch-ext-ap** | Ruckus **T350D** | Bathhouse (outdoor) | Auto | Auto | Auto |

**Управление (VLAN 1):** AP-5 **172.16.122.5**; AP-2 **172.16.122.8**; AP-1 **172.16.122.9**; AP-4 **172.16.122.10**; AP-3 **172.16.122.11**; GW **172.16.122.1**, DNS **172.16.122.254** / **172.16.121.254**. У AP-5 заданы **GPS** 56.075020, 43.532991.

## SSID и настройки

| SSID | Тип | VLAN | Шифрование / аутентификация | Устройства / политики |
|------|-----|------|------------------------------|------------------------|
| **RSW-Union** | Main | **1** | **802.1X (EAP)** • **WPA2/WPA3 mixed** (AES), **802.11w PMF** optional | RADIUS **main-rad**, accounting **main-acc**; **L2 MAC ACL black-list**; band balancing **вкл.**; Wi‑Fi Calling **вкл.** (профили 6,7,8,9,5); до **100** клиентов; привязка радио **2g,5g,6g** |
| **RSW-Country-Base** | IoT | **10** | **WPA2-PSK** (AES), auth **open** (PSK), **802.11w PMF** выкл. | Accounting **main-acc**; **L2 MAC ACL white-list**; до **100** клиентов; **2g,5g,6g** |
| **RSW-Guests** | Guests | **49** | **WPA2/WPA3-PSK mixed** (AES), **802.11w PMF** optional | Локальная БД; **Force DHCP** вкл.; **L2 без ACL**; band balancing **вкл.**; Wi‑Fi Calling **вкл.**; до **25** клиентов; **2g,5g,6g** |
| **RSW-Video** | Video | **50** | **WPA2/WPA3-PSK mixed** (AES + SAE), **802.11w PMF** optional | Accounting **main-acc**; **L2 MAC ACL white-list**; до **100** клиентов; **2g,5g,6g** |

*Пароли и PSK в документ не выносятся — только типы защиты из **`Ruckus.conf`***.

## Покрытие

- **Интерьер:** четыре AP (**два R550**, **два R350**) закрывают гостиную (несколько зон), столовую; радиолинии **2.4 / 5 ГГц** с автовыбором канала и DFS.
- **Экстерьер:** **T350D** на бане, outdoor installation, отдельные диапазоны каналов (см. AP в конфиге), GPS для привязки к месту.
- **Роуминг:** **802.11r FT** включён на перечисленных WLAN; **802.11k** neighbor report включён.
- **Пропускная способность:** на гостевом SSID лимит **25** клиентов; на остальных перечисленных — **100** (кроме гостей).

*Источник: **`sources/Ruckus.conf`**. Имена AP в контексте экосистемы — также `08-ecosystem.md`.*
