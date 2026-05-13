> **Синхронизация:** выровнено с Notion **[Network](https://www.notion.so/35e50b4d73048119b696d7dcd233311b)** (первичный источник). Исходные конфиги — `sources/FGT-61E.conf`, `CG.conf`, `CX.conf`, `ISW16803.conf`, `LTE.conf`.

# Сетевая инфраструктура

## Основное оборудование

| Устройство | Модель | IP-адрес (L3 / управление) | Роль | Порты / uplink (по конфигам) |
|------------|--------|---------------------------|------|--------------------------------|
| Маршрутизатор Pri | Fortinet **FGT-61E** (hostname FGT-61E) | **172.16.122.1** (VLAN 1 / `internal`), GW для IoT/Voice/Mgmt/Guests/Video; **wan1** PPPoE «isp-optic»; **wan2** DHCP «isp-reserv» | Основной шлюз, DHCP, NAT, VPN, политики | Физ. порт **internal7** → стек коммутаторов (hard-switch `internal`); WAN на провайдеров |
| Маршрутизатор Sec | MikroTik **RB912R-2nD**, RouterOS **7.22.2** (`identity` **ch-router-lte**, serial D5940D4DAA23) | **10.10.12.1/24** на `bridge` (DHCP **10.10.12.10–250**, домен `public.bezpalov.com`); LTE **mts** — APN `internet.mts.ru`, IPv4, peer DNS выкл.; **WireGuard** `back-to-home-vpn`, listen **6205/udp** | Резервный WAN (**МТС LTE**), локальный DHCP/NAT при работе через LTE, Wi‑Fi IoT/Video, обратный VPN | **ether1** в `bridge` → **CX Gi0/12** (trunk VLAN **10, 50**, native **155**); **wlan-iot** SSID **RSW-Country-Base** (VLAN 10); **wlan-video** SSID **RSW-Video** (VLAN 50); SNMP **src-address 10.10.12.1**, community ACL **172.16.122.15/32**, **10.10.12.0/24** |
| Коммутатор 1 | Cisco **3560CG-8PC-S** | **172.16.122.252** (SVI Vlan1), **10.254.30.252** (Vlan30 активен); остальные SVI в `shutdown` | L2/L3, DHCP relay → FGT | hostname **ch-switch-01**; uplink **Gi0/9** → CX Gi0/13; **Gi0/10** → ISW16803 |
| Коммутатор 2 | Cisco **3560CX-12PC-S** | **172.16.122.253** (Vlan1), **10.254.30.253** (Vlan30) | L2/L3, первый hop к WAN VLAN и FGT | hostname **ch-switch-02**; **Gi0/1** VLAN 150 «Router WAN Pri»; **Gi0/2** VLAN 155 «Router WAN Sec»; **Gi0/3** trunk → FGT LAN |
| Коммутатор 3 | Extreme **ISW16803** | **10.254.30.4** (Vlan30); Vlan1 **no ip address** | Доступ к камерам / кольцу, SNMP к Zabbix | hostname **ISW16803**; default route **10.254.30.1**; **Gi1/5–1/8** trunks; камеры VLAN 50 на **Gi1/1–1/3** |
| Коммутатор 4 | Dahua **DH-CS4006-4GT-60** | Нет в приложенных `.conf` | PoE / видеокольцо (по топологии) | На **CG** **Gi0/10** description «Uplink 2 (4006)» |
| Минисервер | AMD / **Proxmox VE 9.1.9** | Адрес хоста не задан в switch-конфиге; доступ по VLAN с trunk | Виртуализация | **CG Gi0/2** description «Hypervisor», trunk **1,10,20,30,50** |

## Физическое размещение (инвентаризация, не из `.conf`)

- **Boiler Room (бойлерная = серверная):** коммутационный шкаф; **FortiGate**; **Cisco** **ch-switch-01** и **ch-switch-02**; **PVE** (гипервизор); **NVR**; панель **AX Pro** (охрана).
- **Cabin (бытовка):** **Extreme ISW16803** (коммутатор 3); **MikroTik** **ch-router-lte** (LTE / резервный WAN).
- **Bathhouse, 1-й этаж:** коммутатор **Dahua DH-CS4006-4GT-60** (коммутатор 4).

Сопоставление с зонами — Notion **[Комнаты](https://www.notion.so/35e50b4d730481d98c42c88fecbe07e1)** и `05-rooms.md`.

## LTE / RouterOS (детализация `LTE.conf`)

- **Bridge:** `vlan-filtering=yes`, **IGMP/MLD** snooping, **MVRP**; порты: **ether1** (uplink, `ingress-filtering=no`, trusted), **wlan-iot** PVID **10**, **wlan-video** PVID **50**.
- **Bridge VLAN:** VLAN **10** (IoT) tagged — `bridge`, **ether1**, **wlan-iot**; VLAN **50** (Video) tagged — `bridge`, **ether1**, **wlan-video**; VLAN **1** (Main) untagged — `bridge`, **ether1**.
- **WAN:** интерфейс LTE **`mts`** (базовый `lte1`), roaming off, MTU **1480**; список интерфейсов: **WAN** = `mts`, **LAN** = `bridge`.
- **DHCP:** сервер **Main** на `bridge`, lease **10m**, pool **dhcp** 10.10.12.10–250; в сети DNS для клиентов **208.67.222.222**, **208.67.220.220**, **1.1.1.1**, **1.0.0.1**, NTP **10.10.12.1** (ранее **77.88.8.88**, **77.88.8.2** — сняты).
- **Глобальный DNS** resolver на роутере: **208.67.222.222**, **208.67.220.220**, **1.1.1.1**, **1.0.0.1** (OpenDNS + Cloudflare). **DoH:** `https://doh.opendns.com/dns-query` (*Verify DoH certificate* выкл.; *Allow remote requests* — вкл.). Статическая **router.lan** → **10.10.12.1**. Если в логе есть `DoH server response not OK` / 404 — проверить актуальный DoH URL для связки RouterOS + OpenDNS.
- **Фильтр:** с WAN принимается только уже **DNAT**‑нутый трафик (как на границе); **dst-nat** на **10.254.10.4:80/443** есть, но **disabled=yes**.
- **Прочее:** UPnP включён (internal `bridge`, external `mts`); GPS **enabled** (синхронизация времени); NTP client → `ntp.mscs.ru`; www-ssl/API-ssl на локальных сервисах; **BFD** all interfaces.

## VLAN конфигурация

| VLAN ID | Название (FGT / ISW) | Назначение | DHCP (FortiGate) | IP диапазон / шлюз |
|---------|----------------------|------------|------------------|---------------------|
| 1 | Main (`internal`) | Основная сеть | **Да** (172.16.122.5–250, GW 172.16.122.1, домен `home.bezpalov.com`) | **172.16.122.0/24** |
| 10 | IoT | Умные устройства | **Да** (10.254.10.5–250) | **10.254.10.0/24**, GW **10.254.10.1** |
| 20 | Voice | VoIP / АТС | **Да** (10.254.20.5–250, opt66 provisioning) | **10.254.20.0/24**, GW **10.254.20.1** |
| 30 | Management | Управление | **Да** (10.254.30.5–250) | **10.254.30.0/24**, GW **10.254.30.1** |
| 49 | Guests | Гостевая | **Да** (10.254.49.5–250, DNS OpenDNS/Cloudflare) | **10.254.49.0/24**, GW **10.254.49.1** |
| 50 | Video | Камеры, NVR, охрана | **Да** (10.254.50.5–250, резерв **10.254.50.19**) | **10.254.50.0/24**, GW **10.254.50.1** |
| 150 | WAN_Pri | Линк к основному WAN | Нет (L2 к FGT wan1) | На **CX Gi0/1** access VLAN 150; SVI без IP |
| 155 | WAN_Sec | Линк к LTE‑маршрутизатору | Нет на L3 коммутаторов | **CX Gi0/2** access VLAN 155; к **ch-router-lte** с **CX Gi0/12**: trunk **10, 50**, native **155** |

На **ch-router-lte** дополнительно сеть **10.10.12.0/24** на `bridge` (DHCP-домен `public.bezpalov.com`). Клиенты Wi‑Fi/LTE на этом узле — отдельно от домашних подсетей 10.254.x и 172.16.x.

### VLAN 10 (IoT) — статические хосты

Фиксированные адреса в `10.254.10.0/24` (DHCP-пул на FortiGate **10.254.10.5–250**; см. `sources/FGT-61E.conf`).

| IP | Host | Описание |
|----|------|----------|
| 10.254.10.1 | — | router (шлюз VLAN, FortiGate) |
| 10.254.10.2 | ch-wirenboard | Wirenboard |
| 10.254.10.3 | ch-smart | Home Assistant |
| 10.254.10.4 | ch-waf | EasyWAF |
| 10.254.10.5 | (UI: CH-L2-Gate) | LoRaWAN Lavritech **L2 Gate D2-Lora-ETH**, MQTT на **ch-wirenboard** (**10.254.10.2:1883**) |

**Внимание:** адрес **10.254.10.5** совпадает с нижней границей DHCP-пула VLAN 10 на FortiGate — нужна резервация этого IP или сдвиг пула (например с **10.254.10.10**).

*Детали Wiren Board, LoRaWAN (Modbus, MQTT):* Notion **[Устройства](https://www.notion.so/35e50b4d730481ccbf81cdff3889dcad)** и `07-wirenboard.md`.

## DNS серверы

| Роль | IP-адрес | Примечания |
|------|----------|------------|
| Primary DNS | 172.16.122.254 | В `system dhcp server` на FortiGate для внутренних VLAN; совпадает с ISW16803 `ip name-server 0` |
| Secondary DNS | 172.16.121.254 | Резерв |
| Tertiary DNS | 172.16.120.2 | Третий резерв |

## Port mapping (DNAT, `config firewall vip`, внешний IP **176.112.106.71**)

| Имя VIP | Внешний порт / протокол | Внутренний адрес | Внутренний порт |
|---------|-------------------------|------------------|-----------------|
| CH WAF HTTP | 80 TCP | 10.254.10.4 | 80 |
| CH WAF HTTPS | 443 TCP | 10.254.10.4 | 443 |
| CH 3CX 5001 | 5001 TCP | 10.254.20.2 | 5001 |
| CH 3CX 5060 | 5060 TCP | 10.254.20.2 | 5060 |
| CH 3CX 5061 | 5061 TCP | 10.254.20.2 | 5061 |
| CH 3CX 5060 UDP | 5060 UDP | 10.254.20.2 | 5060 |
| CH 3CX 5090 | 5090 TCP | 10.254.20.2 | 5090 |
| CH 3CX 5090 UDP | 5090 UDP | 10.254.20.2 | 5090 |
| CH 3CX Media Ports | 9000–10999 UDP | 10.254.20.2 | 9000–10999 |
| CH TrueNAS 51413 | 51413 TCP | 172.16.122.4 | 51413 |
| CH TrueNAS 51413 UDP | 51413 UDP | 172.16.122.4 | 51413 |
| CH Zabbix Server | 10050–10053 TCP | 172.16.122.15 | 10050–10053 |

## Ключевые порты доступа (описания на коммутаторах)

- **ch-switch-01 (3560CG):** Gi0/2 Hypervisor; Gi0/3 NVR; Gi0/4 IPCam; Gi0/5–0/8 AP; Gi0/9 uplink CX; Gi0/10 uplink ISW16803.
- **ch-switch-02 (3560CX):** Gi0/1 WAN Pri; Gi0/2 WAN Sec; Gi0/3 Router (LAN) trunk к FGT; Gi0/12 Mikrotik LTE/AP; Gi0/13 uplink к 3560CG; порты доступа IoT/Video/телефонии — см. description в `sources/CX.conf`.

*Источники: **`FGT-61E.conf`**, **`CG.conf`**, **`CX.conf`**, **`ISW16803.conf`**, **`LTE.conf`** (снимки конфигурации).*
