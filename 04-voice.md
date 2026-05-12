Используя Notion MCP, создай на странице "Voice" следующую структуру:

# 🎤 Голосовая инфраструктура (VoIP)

Консоль: **https://bezpalov.3cx.eu:5001/**

## 📞 АТС (IP-телефония)

| Параметр | Значение |
|----------|----------|
| **Тип АТС** | 3CX |
| **Версия** | 20 (WebRTC proxy fw **20.0.9.873** на экране Phones) |
| **Размещение** | VLAN 20; хост/ВМ — см. страницу **Network** |
| **IP-адрес** | 10.254.20.2 |
| **Порты** | HTTPS: **5001** (веб), SIP: **5060/5061**, Tunnel: **5090** |
| **Лицензия** | AI Edition |
| **Мосты** | WebMeeting (Master); **HQ** (Slave bridge over tunnel) |
| **Исходящие** | Маршрут **HQ** (см. Outbound Rules в консоли) |
| **Статус** | ✅ Активен |

## 👥 Пользователи (Users)

| Пользователь | Роль | Email | Ext | Отделы |
|--------------|------|-------|-----|---------|
| Operator, System | System Owner | operator@bezpalov.com | 100 | DEFAULT, Operators |
| Bezpalov, Sergey | Manager | sergey@bezpalov.com | 101 | DEFAULT |
| Bezpalova, Irina | Manager | irina@bezpalov.com | 102 | DEFAULT |
| Bezpalov, Alexandr | User | alexandr@bezpalov.com | 103 | DEFAULT |
| Bezpalov, Alexey | User | alexey@bezpalov.com | 104 | DEFAULT |
| Bazankova, Tat'yana | User | — | 105 | DEFAULT |
| Bazankova, Anna | User | — | 106 | DEFAULT |

## 📱 Клиенты (Phones — фрагмент консоли)

| Ext | Vendor | Model | Fw | Name |
|-----|--------|-------|-----|------|
| 196 | 3CX | WebRTC proxy | 20.0.9.873 | Gold, Anna |
| 197 | 3CX | WebRTC proxy | 20.0.9.873 | Bond, James |

## 📤 Outbound Rules

| Имя | Prefix | Call from | Length | Route 1 |
|-----|--------|-----------|--------|---------|
| 1XXX | 1 | All | 4 | HQ |
| 2XXX | 2 | All | 4 | HQ |
| City Call | Any | All | 7 | HQ |
| National | 8 | All | 11 | HQ |
| International | 810 | **101–102** | 14 | HQ |

## ☎️ Call Handling

| Name | Extension | Department |
|------|-----------|------------|
| Hikvision | GRP0000 | Hikvision |
| DEFAULT | GRP2 | DEFAULT |
| Operators | GRP35 | Operators |

## 🏢 Departments

- **DEFAULT** — основные пользователи семьи.
- **Hikvision** — отдел под интеграции/группу приёма вызовов (Office Hours: Configured).
- **Operators** — System Operator, Bond James.

## 🌐 Настройки сети

| Параметр | Значение |
|----------|----------|
| **VLAN** | 20 (Voice), GW **10.254.20.1** (FortiGate) |

## 🔧 Дополнительная информация

- Международная **810** (14 цифр) — только с **101–102**.
- Публичный веб и SIP — см. VIP **CH 3CX** на странице **Network**.

## 📝 Заметки

- Дописать реальные SIP-транки, если появятся отдельно от маршрута **HQ**.
- Актуальная полная версия — Notion **Voice**.
