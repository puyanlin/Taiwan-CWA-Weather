"""CWA Weather sensors."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_CITY, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    city = entry.data[CONF_CITY]
    async_add_entities(
        [
            CWAWeatherSensor(coordinator, entry, city, "weather"),
            CWARainProbSensor(coordinator, entry, city),
            CWAMinTempSensor(coordinator, entry, city),
            CWAMaxTempSensor(coordinator, entry, city),
        ]
    )


class CWABaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, city: str, key: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._city = city
        self._entry = entry

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": f"CWA Weather {self._city}",
            "manufacturer": "Central Weather Administration",
            "model": "F-C0032-001",
        }

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success

    @property
    def _data(self):
        return self.coordinator.data or {}


class CWAWeatherSensor(CWABaseSensor):
    _attr_icon = "mdi:weather-partly-cloudy"

    def __init__(self, coordinator, entry, city, key):
        super().__init__(coordinator, entry, city, key)
        self._attr_unique_id = f"{entry.entry_id}_weather"
        self._attr_name = f"CWA Weather {city}"
        self.entity_id = "sensor.cwa_weather"

    @property
    def state(self):
        return self._data.get("weather")


class CWARainProbSensor(CWABaseSensor):
    _attr_icon = "mdi:weather-rainy"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, entry, city):
        super().__init__(coordinator, entry, city, "rain_prob")
        self._attr_unique_id = f"{entry.entry_id}_rain_prob"
        self._attr_name = f"CWA Rain Probability {city}"
        self.entity_id = "sensor.cwa_rain_prob"

    @property
    def native_value(self):
        val = self._data.get("rain_prob")
        try:
            return int(val)
        except (TypeError, ValueError):
            return None


class CWAMinTempSensor(CWABaseSensor):
    _attr_icon = "mdi:thermometer-low"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, entry, city):
        super().__init__(coordinator, entry, city, "min_temp")
        self._attr_unique_id = f"{entry.entry_id}_min_temp"
        self._attr_name = f"CWA Min Temperature {city}"
        self.entity_id = "sensor.cwa_min_temp"

    @property
    def native_value(self):
        val = self._data.get("min_temp")
        try:
            return float(val)
        except (TypeError, ValueError):
            return None


class CWAMaxTempSensor(CWABaseSensor):
    _attr_icon = "mdi:thermometer-high"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, entry, city):
        super().__init__(coordinator, entry, city, "max_temp")
        self._attr_unique_id = f"{entry.entry_id}_max_temp"
        self._attr_name = f"CWA Max Temperature {city}"
        self.entity_id = "sensor.cwa_max_temp"

    @property
    def native_value(self):
        val = self._data.get("max_temp")
        try:
            return float(val)
        except (TypeError, ValueError):
            return None
