"""Taiwan CWA Weather integration for Home Assistant."""
from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CITY_SLUGS,
    CONF_API_KEY,
    CONF_CITIES,
    CONF_SCAN_INTERVAL,
    CWA_API_URL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api_key = entry.data[CONF_API_KEY]
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    cities = entry.options.get(CONF_CITIES, [])

    _async_cleanup_stale_devices(hass, entry, cities)

    coordinators: dict[str, CWAWeatherCoordinator] = {}
    for city in cities:
        coordinator = CWAWeatherCoordinator(
            hass, api_key=api_key, city=city, scan_interval=scan_interval
        )
        await coordinator.async_config_entry_first_refresh()
        coordinators[city] = coordinator

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinators

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


def _async_cleanup_stale_devices(
    hass: HomeAssistant, entry: ConfigEntry, cities: list[str]
) -> None:
    """Remove devices for cities that are no longer selected."""
    active_identifiers = {
        f"{entry.entry_id}_{CITY_SLUGS.get(city, city)}" for city in cities
    }
    dev_reg = dr.async_get(hass)
    for device in list(dr.async_entries_for_config_entry(dev_reg, entry.entry_id)):
        if not any(
            domain == DOMAIN and identifier in active_identifiers
            for domain, identifier in device.identifiers
        ):
            dev_reg.async_remove_device(device.id)


class CWAWeatherCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        city: str,
        scan_interval: int,
    ) -> None:
        self.api_key = api_key
        self.city = city
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{city}",
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict:
        params = {
            "Authorization": self.api_key,
            "locationName": self.city,
            "format": "JSON",
        }
        connector = aiohttp.TCPConnector(ssl=False)
        try:
            async with async_timeout.timeout(30):
                async with aiohttp.ClientSession(connector=connector) as session:
                    async with session.get(CWA_API_URL, params=params) as resp:
                        if resp.status != 200:
                            raise UpdateFailed(f"CWA API returned {resp.status}")
                        data = await resp.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"CWA API request failed: {err}") from err

        try:
            location = data["records"]["location"][0]
            elements = location["weatherElement"]
            return {
                "weather": elements[0]["time"][0]["parameter"]["parameterName"],
                "rain_prob": elements[1]["time"][0]["parameter"]["parameterName"],
                "min_temp": elements[2]["time"][0]["parameter"]["parameterName"],
                "max_temp": elements[4]["time"][0]["parameter"]["parameterName"],
            }
        except (KeyError, IndexError) as err:
            raise UpdateFailed(f"Unexpected CWA API response structure: {err}") from err
