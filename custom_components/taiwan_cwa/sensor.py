"""Taiwan CWA Weather sensors."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CITY_SLUGS, CONF_CITIES, DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinators: dict = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for city, coordinator in coordinators.items():
        slug = CITY_SLUGS.get(city, city)
        entities.extend(
            [
                CWAWeatherSensor(coordinator, entry, city, slug),
                CWARainProbSensor(coordinator, entry, city, slug),
                CWAMinTempSensor(coordinator, entry, city, slug),
                CWAMaxTempSensor(coordinator, entry, city, slug),
            ]
        )
    async_add_entities(entities)


class CWABaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, city: str, slug: str, key: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._city = city
        self._slug = slug
        self._entry = entry

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"{self._entry.entry_id}_{self._slug}")},
            "name": f"Taiwan CWA Weather {self._city}",
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

    def __init__(self, coordinator, entry, city, slug):
        super().__init__(coordinator, entry, city, slug, "weather")
        self._attr_unique_id = f"{entry.entry_id}_{slug}_weather"
        self._attr_name = f"Taiwan CWA {city} Weather"
        self.entity_id = f"sensor.taiwan_cwa_{slug}_weather"

    @property
    def state(self):
        return self._data.get("weather")


class CWARainProbSensor(CWABaseSensor):
    _attr_icon = "mdi:weather-rainy"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator, entry, city, slug):
        super().__init__(coordinator, entry, city, slug, "rain_prob")
        self._attr_unique_id = f"{entry.entry_id}_{slug}_rain_prob"
        self._attr_name = f"Taiwan CWA {city} Rain Probability"
        self.entity_id = f"sensor.taiwan_cwa_{slug}_rain_prob"

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

    def __init__(self, coordinator, entry, city, slug):
        super().__init__(coordinator, entry, city, slug, "min_temp")
        self._attr_unique_id = f"{entry.entry_id}_{slug}_min_temp"
        self._attr_name = f"Taiwan CWA {city} Min Temperature"
        self.entity_id = f"sensor.taiwan_cwa_{slug}_min_temp"

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

    def __init__(self, coordinator, entry, city, slug):
        super().__init__(coordinator, entry, city, slug, "max_temp")
        self._attr_unique_id = f"{entry.entry_id}_{slug}_max_temp"
        self._attr_name = f"Taiwan CWA {city} Max Temperature"
        self.entity_id = f"sensor.taiwan_cwa_{slug}_max_temp"

    @property
    def native_value(self):
        val = self._data.get("max_temp")
        try:
            return float(val)
        except (TypeError, ValueError):
            return None
