"""Taiwan CWA Weather integration for Home Assistant."""
from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_API_KEY,
    CONF_CITY,
    CONF_SCAN_INTERVAL,
    CWA_API_URL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api_key = entry.data[CONF_API_KEY]
    city = entry.data[CONF_CITY]
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    coordinator = CWAWeatherCoordinator(
        hass, api_key=api_key, city=city, scan_interval=scan_interval
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


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
            name=DOMAIN,
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
