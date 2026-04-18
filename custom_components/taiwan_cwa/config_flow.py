"""Config flow for Taiwan CWA Weather integration."""
from __future__ import annotations

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import (
    CITIES,
    CONF_API_KEY,
    CONF_CITY,
    CONF_SCAN_INTERVAL,
    CWA_API_URL,
    DEFAULT_CITY,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)


async def _validate_api_key(api_key: str, city: str) -> str | None:
    """Return error string or None if valid."""
    params = {"Authorization": api_key, "locationName": city, "format": "JSON"}
    connector = aiohttp.TCPConnector(ssl=False)
    try:
        async with async_timeout.timeout(15):
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(CWA_API_URL, params=params) as resp:
                    if resp.status == 401:
                        return "invalid_auth"
                    if resp.status != 200:
                        return "cannot_connect"
                    data = await resp.json()
                    if not data.get("records", {}).get("location"):
                        return "city_not_found"
    except (aiohttp.ClientError, TimeoutError):
        return "cannot_connect"
    return None


class CWAWeatherConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            error = await _validate_api_key(
                user_input[CONF_API_KEY], user_input[CONF_CITY]
            )
            if error:
                errors["base"] = error
            else:
                await self.async_set_unique_id(
                    f"{user_input[CONF_API_KEY][:8]}_{user_input[CONF_CITY]}"
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"Taiwan CWA Weather – {user_input[CONF_CITY]}",
                    data=user_input,
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_CITY, default=DEFAULT_CITY): vol.In(CITIES),
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.All(vol.Coerce(int), vol.Range(min=300, max=86400)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
