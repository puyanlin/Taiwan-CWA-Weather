# Taiwan CWA Weather — Home Assistant Custom Integration

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=puyanlin&repository=Taiwan-CWA-Weather&category=integration)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

透過中央氣象署（CWA）開放資料 API，為 Home Assistant 提供臺灣天氣預報 sensor。

---

## 提供的 Sensor

| Entity ID | 說明 | 單位 |
|---|---|---|
| `sensor.taiwan_cwa_weather` | 天氣狀況（如「陰短暫陣雨」） | — |
| `sensor.taiwan_cwa_rain_prob` | 降雨機率 | % |
| `sensor.taiwan_cwa_min_temp` | 今日最低溫 | °C |
| `sensor.taiwan_cwa_max_temp` | 今日最高溫 | °C |

---

## 取得 CWA API 金鑰

1. 前往 [中央氣象署開放資料平臺](https://opendata.cwa.gov.tw/)
2. 點選右上角「**登入/註冊**」，建立免費帳號
3. 登入後點選右上角帳號名稱 → 「**取得授權碼**」
4. 複製您的 API 授權碼（格式類似 `CWA-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`）

---

## 安裝方式

### 方法一：透過 HACS（建議）

1. 在 Home Assistant 中開啟 **HACS**
2. 點選右上角 **⋮** → **Custom repositories**
3. 輸入此 repo URL，類型選 **Integration**，按 **ADD**
4. 搜尋 **Taiwan CWA Weather** 並安裝
5. 重新啟動 Home Assistant

### 方法二：手動安裝

1. 下載此 repo 並解壓縮
2. 將 `custom_components/taiwan_cwa/` 整個目錄複製到您 HA 設定目錄的 `custom_components/` 下：
   ```
   config/
   └── custom_components/
       └── taiwan_cwa/
           ├── __init__.py
           ├── manifest.json
           ├── config_flow.py
           ├── sensor.py
           ├── const.py
           └── translations/
   ```
3. 重新啟動 Home Assistant

---

## 設定

1. 前往 **設定 → 裝置與服務 → 新增整合**
2. 搜尋 **Taiwan CWA Weather**
3. 填入：
   - **CWA API 金鑰**：您的 CWA 授權碼
   - **城市**：從下拉選單選擇（預設：臺北市）
   - **更新間隔**：資料更新頻率（秒，預設 3600，最小 300）

---

## 支援城市

| | | |
|---|---|---|
| 臺北市 | 新北市 | 桃園市 |
| 臺中市 | 臺南市 | 高雄市 |
| 基隆市 | 新竹市 | 嘉義市 |
| 新竹縣 | 苗栗縣 | 彰化縣 |
| 南投縣 | 雲林縣 | 嘉義縣 |
| 屏東縣 | 宜蘭縣 | 花蓮縣 |
| 臺東縣 | 澎湖縣 | 金門縣 |
| 連江縣 | | |

---

## 注意事項

- 此整合使用 CWA F-C0032-001 資料集（一般天氣預報-縣市預報資料）
- 因 CWA 伺服器憑證缺少 Subject Key Identifier extension，連線時略過 SSL 驗證（`ssl=False`）
- 天氣資料為當日第一個預報時段（通常為 12 小時區間）

---

## License

MIT
