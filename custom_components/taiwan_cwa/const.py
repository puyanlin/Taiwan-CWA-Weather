"""Constants and shared helpers for the Taiwan CWA Weather integration."""
from __future__ import annotations

import ssl

from homeassistant.core import HomeAssistant

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

CITY_EN_NAMES = {
    "臺北市": "Taipei City",
    "新北市": "New Taipei City",
    "桃園市": "Taoyuan City",
    "臺中市": "Taichung City",
    "臺南市": "Tainan City",
    "高雄市": "Kaohsiung City",
    "基隆市": "Keelung City",
    "新竹市": "Hsinchu City",
    "嘉義市": "Chiayi City",
    "新竹縣": "Hsinchu County",
    "苗栗縣": "Miaoli County",
    "彰化縣": "Changhua County",
    "南投縣": "Nantou County",
    "雲林縣": "Yunlin County",
    "嘉義縣": "Chiayi County",
    "屏東縣": "Pingtung County",
    "宜蘭縣": "Yilan County",
    "花蓮縣": "Hualien County",
    "臺東縣": "Taitung County",
    "澎湖縣": "Penghu County",
    "金門縣": "Kinmen County",
    "連江縣": "Lienchiang County",
}

CITY_OPTIONS = [
    {"value": name, "label": f"{name} ({CITY_EN_NAMES[name]})"} for name in CITIES
]

SENSOR_WEATHER = "weather"
SENSOR_RAIN_PROB = "rain_prob"
SENSOR_MIN_TEMP = "min_temp"
SENSOR_MAX_TEMP = "max_temp"

# TWCA certificate chain for opendata.cwa.gov.tw.
#
# The CWA endpoint is served by a certificate that chains up to the
# "TWCA Global Root CA". We bundle that root together with its
# "TWCA Secure SSL Certification Authority" intermediate so TLS verification
# still succeeds when either:
#   * the Home Assistant host has an outdated CA store that predates the
#     TWCA Global Root CA, or
#   * the CWA server intermittently omits the intermediate certificate
#     (Python, unlike desktop browsers, does not fetch missing intermediates
#     via the AIA extension).
# This keeps full certificate verification — the chain always terminates at
# the publicly trusted TWCA Global Root CA — so the API key is never sent over
# an unverified TLS connection. The bundle is additive: if CWA rotates to a
# different chain in the future, the host's own CA store still verifies it.
TWCA_CA_BUNDLE = """\
-----BEGIN CERTIFICATE-----
MIIFQTCCAymgAwIBAgICDL4wDQYJKoZIhvcNAQELBQAwUTELMAkGA1UEBhMCVFcx
EjAQBgNVBAoTCVRBSVdBTi1DQTEQMA4GA1UECxMHUm9vdCBDQTEcMBoGA1UEAxMT
VFdDQSBHbG9iYWwgUm9vdCBDQTAeFw0xMjA2MjcwNjI4MzNaFw0zMDEyMzExNTU5
NTlaMFExCzAJBgNVBAYTAlRXMRIwEAYDVQQKEwlUQUlXQU4tQ0ExEDAOBgNVBAsT
B1Jvb3QgQ0ExHDAaBgNVBAMTE1RXQ0EgR2xvYmFsIFJvb3QgQ0EwggIiMA0GCSqG
SIb3DQEBAQUAA4ICDwAwggIKAoICAQCwBdvI64zEbooh745NnHEKH1Jw7W2CnJfF
10xORUnLQEK1EjRsGcJ0pDFfhQKX7EMzClPSnIyOt7h52yvVavKOZsTuKwEHktSz
0ALfUPZVr2YOy+BHYC8rMjk1Ujoog/h7FsYYuGLWRyWRzvAZEk2tY/XTP3VfKfCh
MBwqoJimFb3u/Rk28OKRQ4/6ytYQJ0lM793B8YVwm8rqqFpD/G2Gb3PpN0Wp8DbH
zIh1HrtsBv+baz4X7GGqcXzGHaL3SekVtTzWoWH1EfcFbx39Eb7QMAfCKbAJTibc
46KokWofwpFFiFzlmLhxpRUZyXx1EcxwdE8tmx2RRP1WKKD+u4ZqyPpcC1jcxkt2
yKsi2XMPpfRaAok/T54igu6idFMqPVMnaR1sjjIsZAAmY2E2TqNGtz99sy2sbZCi
laLOz9qC5wc0GZbpuCGqKX6mOL6OKUohZnkfs8O1CWfe1tQHRvMq2uYiN2DLgbYP
oA/pyJV/v1WRBXrPPRXAb94JlAGD1zQbzECl8LibZ9WYkTunhHiVJqRaCPgrdLQA
BDzfuBSO6N+pjWxnkjMdwLfS7JLIvgm/LCkFbwJrnu+8vyq8W8BQj0FwcYeyTbcE
qYSjMq+u7msXi7Kx/mzhkIyIqJdIzshNy/MGz19qCkKxHh53L46g5pIOBvwFItIm
4TFRfTLcDwIDAQABoyMwITAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0TAQH/BAUwAwEB
/zANBgkqhkiG9w0BAQsFAAOCAgEAXzSBdu+WHdXltdkCY4QWwa6gcFGn90xHNcgL
1yg9iXHZqjNB6hQbbCEAwGxCGX6faVsgQt+i0trEfJdLjbDorMjupWkEmQqSpqsn
LhpNgb+E1HAerUf+/UqdM+DyucRFCCEK2mlpc3INvjT+lIutwx4116KD7+U4x6WF
H6vPNOw/KP4M8VeGTslV9xzU2KV9Bnpv1d8Q34FOIWWxtuEXeZVFBs5fzNxGiWNo
RI2T9GRwoD2dKAXDOXC4Ynsg/eTb6QihuJ49CcdP+yz4k3ZB3lLg4VfSnQO8d57+
nile98FRYB/e2guyLXW3Q0iT5/Z5xoRdgFlglPx4mI88k1HtQJAH32RjJMtOcQWh
15QaiDLxInQirqWm2BJpTGCjAu4r7NRjkgtevi92a6O2JryPA9gK8kxkRr05YuWW
6zRjESjMlfGt7+/cgFhI6Uu46mWs6fyAtbXIRfmswZ/ZuepiiI7E8UuDEq3mi4TW
nsLrgxifarsbJGAzcMzs9zLzXNl5fe+epP7JI8Mk7hWSsT2RTyaGvWZzJBPqpK5j
wa19hAM8EHiGG3njxPPyBJUgriOCxLM6AGK/5jYk4Ve6xx6QddVfP5VhK8E7zeWz
aGHQRiapIVJpLesux+t3zqY6tQMzT3bR51xUAV3LePTJDL/PEo4XLSNolOer/qmy
KwbQBM0=
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIFxjCCA66gAwIBAgIQQAE0s2gAAAAAAAAM0KoI7DANBgkqhkiG9w0BAQsFADBR
MQswCQYDVQQGEwJUVzESMBAGA1UEChMJVEFJV0FOLUNBMRAwDgYDVQQLEwdSb290
IENBMRwwGgYDVQQDExNUV0NBIEdsb2JhbCBSb290IENBMB4XDTIzMTAxNjA5MDEw
NFoXDTMwMTAxNjE1NTk1OVowUzELMAkGA1UEBhMCVFcxEjAQBgNVBAoTCVRBSVdB
Ti1DQTEwMC4GA1UEAxMnVFdDQSBTZWN1cmUgU1NMIENlcnRpZmljYXRpb24gQXV0
aG9yaXR5MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyS5amjYQhd10
hZs00r7RXdI3ASka2AQmJnOyA6bqvAYOMlMECUdlsjDccdmMdHx8YTYYMtmCy+UB
RJZ/ytVANVQlfcUvXzWfauFs8XpCC/Th+Ed2tIEEGK218QsBebImAHPGDvp2Yglj
XVaQR/0FeN1lIzQ3iUkad0dCsC/bxFiWsmsjeSscTaxrYzHFADUhK0qj4W5PmOuw
lAR3C4XXgzPAI3V0qBpQ7sqgNLaNBFTZkP6AVryZC+DapfWBIMmIxIOg8g25MKb4
XvXkCLYKIxi8Djhv1zSmLLrKbQFZrjWlD/OWqInPPmSwBrKZ13EMQhoRRi1pXfN+
J2ugR/PUQQIDAQABo4IBljCCAZIwHwYDVR0jBBgwFoAUSNvN3o7pSXJaiOix2D0H
s7lrZlAwHQYDVR0OBBYEFJLn+mIWcYzzl3FCxgan4EZhS1y2MA4GA1UdDwEB/wQE
AwIBhjAdBgNVHSUEFjAUBggrBgEFBQcDAQYIKwYBBQUHAwIwSgYDVR0gBEMwQTA1
BgsrBgEEAYK/JQEBFTAmMCQGCCsGAQUFBwIBFhhodHRwczovL3d3dy50d2NhLmNv
bS50dy8wCAYGZ4EMAQICMEkGA1UdHwRCMEAwPqA8oDqGOGh0dHA6Ly9yb290Y2Eu
dHdjYS5jb20udHcvVFdDQVJDQS9nbG9iYWxfcmV2b2tlXzQwOTYuY3JsMBIGA1Ud
EwEB/wQIMAYBAf8CAQAwdgYIKwYBBQUHAQEEajBoMDwGCCsGAQUFBzAChjBodHRw
Oi8vc3Nsc2VydmVyLnR3Y2EuY29tLnR3L2NhY2VydC9yb290NDA5Ni5jcnQwKAYI
KwYBBQUHMAGGHGh0dHA6Ly9yb290b2NzcC50d2NhLmNvbS50dy8wDQYJKoZIhvcN
AQELBQADggIBADVzQW2rRsMiWoVrBdZX1BiOgN6B/Ryt2zpq8uRxFQspvGYfUVIm
4uU4AaPR7aQ5KwpKjDWv2ncvX2ssCY54B82g2mxEEVEdu5PFl0jkuk4LmPsClYZc
6J6odUbVI3wtv2yF6+fqQrO+gDhEIhlg3IqWICfiyJZS+p2TirMszGzs4a+K9tZX
rS2W/jKsSt4bSmcIzDpwm2gSaSuLDIAwq0WrD29kA7+N+rMMs4zBIVKyYm9r08q4
UOGU16J7mKBrF0KYDZFyT9Hq5HAX2uwYoQJxQ5Z0BR8eZH8AIIi2vsFC8pkv2ra1
2dldd3Pivm0mdratbn1Z6MQ71FKR9Ui3L8P+0xu8DkhhxE11Ogpl+aquBUqGcvlD
0SgpXy+eoeFaRhFXRUkWtH/3XYo+h+N+4jZmgjCLd4+YI+u5tbUGpyBMABmUDiqZ
xcrPGc4cvXExqYePUg6cFCDcjqGCxqSu5BPbA5R+DSTkn5Sc1WQzORJpD5b7pcEq
8msolev88dcmddLXMyWzXQfPHA4vaQD74lr5LIzn6BRjVv+ZB7Y0ZTnnOimDXxn7
Cxqd+1/8ldRis/tO/JWZsMm5ruvCppwCZUdXjSNI5R1OxzVwTVLzsCoiSYPV0agd
a5dQ9wayB6OohBK7+ZU2V3sZwE2xwHdDzfhbdzmI++TxtOurDHbkfkED
-----END CERTIFICATE-----
"""

_cwa_ssl_context: ssl.SSLContext | None = None


def _build_cwa_ssl_context() -> ssl.SSLContext:
    """Create a verifying SSL context augmented with the TWCA chain."""
    context = ssl.create_default_context()
    context.load_verify_locations(cadata=TWCA_CA_BUNDLE)
    return context


async def async_get_cwa_ssl_context(hass: HomeAssistant) -> ssl.SSLContext:
    """Return a cached verifying SSL context that trusts the TWCA chain.

    Built once in the executor because create_default_context() reads the
    system CA bundle from disk, which must not block the event loop.
    """
    global _cwa_ssl_context
    if _cwa_ssl_context is None:
        _cwa_ssl_context = await hass.async_add_executor_job(_build_cwa_ssl_context)
    return _cwa_ssl_context
