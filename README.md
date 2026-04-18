# Taiwan CWA Weather

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=puyanlin&repository=Taiwan-CWA-Weather&category=integration)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

A Home Assistant custom integration for Taiwan Central Weather Administration (中央氣象署, CWA) weather data.  
台灣中央氣象署天氣資料的 Home Assistant 自訂整合。

---

## Features / 功能

- Current weather condition / 目前天氣狀況（例：陰短暫陣雨）
- Rain probability / 降雨機率（%）
- Max temperature / 最高溫（°C）
- Min temperature / 最低溫（°C）
- Configurable update interval / 可自訂更新頻率
- Supports all 22 cities/counties in Taiwan / 支援台灣全部 22 縣市

---

## Installation via HACS / 透過 HACS 安裝

### One-click / 一鍵安裝

Click the button above / 點擊上方按鈕，HA 會自動打開 HACS 安裝對話框。

### Manual HACS / 手動 HACS

1. Open HACS → Integrations / 開啟 HACS → 整合
2. Click the three-dot menu → Custom Repositories / 點選右上角三點選單 → 自訂存放庫
3. Enter URL: `https://github.com/puyanlin/Taiwan-CWA-Weather` / 輸入上方網址
4. Category: Integration / 類別選「整合」
5. Click Add, then find and download "Taiwan CWA Weather" / 點新增，找到後下載
6. Restart Home Assistant / 重啟 Home Assistant

### Manual / 手動安裝

Copy `custom_components/taiwan_cwa/` to your HA `config/custom_components/` folder, then restart.  
將 `custom_components/taiwan_cwa/` 複製到 HA 的 `config/custom_components/` 後重啟。

---

## Configuration / 設定

After installation, go to **Settings → Integrations → Add Integration** and search for **Taiwan CWA Weather**.  
安裝後前往 **設定 → 整合 → 新增整合**，搜尋 **Taiwan CWA Weather**。

You will need: / 需要填入：
- **CWA API Key** — Get it free at [opendata.cwa.gov.tw](https://opendata.cwa.gov.tw/) / 免費申請
- **City / 城市** — Select from dropdown (22 options) / 從下拉選單選擇（22 縣市）
- **Update interval / 更新間隔** — Default 3600 seconds / 預設 3600 秒

---

## Sensors / 感應器

| Entity ID | Description | 說明 |
|---|---|---|
| `sensor.taiwan_cwa_weather` | Weather condition | 天氣狀況 |
| `sensor.taiwan_cwa_rain_prob` | Rain probability (%) | 降雨機率 |
| `sensor.taiwan_cwa_max_temp` | Max temperature (°C) | 最高溫 |
| `sensor.taiwan_cwa_min_temp` | Min temperature (°C) | 最低溫 |

---

## Supported Cities / 支援縣市

臺北市、新北市、桃園市、臺中市、臺南市、高雄市、基隆市、新竹市、新竹縣、苗栗縣、彰化縣、南投縣、雲林縣、嘉義市、嘉義縣、屏東縣、宜蘭縣、花蓮縣、臺東縣、澎湖縣、金門縣、連江縣

---

## Notes / 注意事項

- CWA's SSL certificate is missing the Subject Key Identifier extension. This integration disables SSL verification for the CWA API endpoint only.  
  CWA 官方 API 的 SSL 憑證缺少 Subject Key Identifier，本整合僅針對該 API 停用 SSL 驗證。
- Data is sourced from the F-C0032-001 dataset (36-hour forecast).  
  資料來源為 F-C0032-001（36小時預報）。

---

## License

MIT
