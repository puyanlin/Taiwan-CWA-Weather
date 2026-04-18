DOMAIN = "taiwan_cwa"
CONF_API_KEY = "api_key"
CONF_CITY = "city"
CONF_CITIES = "cities"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_CITY = "臺北市"
DEFAULT_SCAN_INTERVAL = 3600

CWA_API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"

CITIES = [
    "臺北市",
    "新北市",
    "桃園市",
    "臺中市",
    "臺南市",
    "高雄市",
    "基隆市",
    "新竹市",
    "嘉義市",
    "新竹縣",
    "苗栗縣",
    "彰化縣",
    "南投縣",
    "雲林縣",
    "嘉義縣",
    "屏東縣",
    "宜蘭縣",
    "花蓮縣",
    "臺東縣",
    "澎湖縣",
    "金門縣",
    "連江縣",
]

CITY_SLUGS = {
    "臺北市": "taipei",
    "新北市": "new_taipei",
    "桃園市": "taoyuan",
    "臺中市": "taichung",
    "臺南市": "tainan",
    "高雄市": "kaohsiung",
    "基隆市": "keelung",
    "新竹市": "hsinchu_city",
    "嘉義市": "chiayi_city",
    "新竹縣": "hsinchu_county",
    "苗栗縣": "miaoli",
    "彰化縣": "changhua",
    "南投縣": "nantou",
    "雲林縣": "yunlin",
    "嘉義縣": "chiayi_county",
    "屏東縣": "pingtung",
    "宜蘭縣": "yilan",
    "花蓮縣": "hualien",
    "臺東縣": "taitung",
    "澎湖縣": "penghu",
    "金門縣": "kinmen",
    "連江縣": "lienchiang",
}

SENSOR_WEATHER = "weather"
SENSOR_RAIN_PROB = "rain_prob"
SENSOR_MIN_TEMP = "min_temp"
SENSOR_MAX_TEMP = "max_temp"
