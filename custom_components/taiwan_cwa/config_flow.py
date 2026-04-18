"""Config flow for Taiwan CWA Weather integration."""
from __future__ import annotations

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CITY_EN_NAMES,
    CITY_OPTIONS,
    CONF_API_KEY,
    CONF_CITIES,
    CONF_CITY,
    CONF_SCAN_INTERVAL,
    CWA_API_URL,
    DEFAULT_CITY,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)


async def _validate_api_key(api_key: str, city: str) -> str | None:
    """Return error key or None if valid."""
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

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> CWAWeatherOptionsFlow:
        return CWAWeatherOptionsFlow()

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            initial_city = user_input[CONF_CITY]
            error = await _validate_api_key(user_input[CONF_API_KEY], initial_city)
            if error:
                errors["base"] = error
            else:
                await self.async_set_unique_id(user_input[CONF_API_KEY][:8])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title="Taiwan CWA Weather",
                    data={
                        CONF_API_KEY: user_input[CONF_API_KEY],
                        CONF_SCAN_INTERVAL: user_input.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    },
                    options={CONF_CITIES: [initial_city]},
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_CITY, default=DEFAULT_CITY): SelectSelector(
                    SelectSelectorConfig(
                        options=CITY_OPTIONS,
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.All(vol.Coerce(int), vol.Range(min=300, max=86400)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "opendata_host": "opendata.cwa.gov.tw",
                "opendata_url": "https://opendata.cwa.gov.tw/",
            },
        )


class CWAWeatherOptionsFlow(config_entries.OptionsFlow):
    def __init__(self) -> None:
        self._pending_cities: list[str] | None = None

    async def async_step_init(self, user_input=None):
        errors = {}
        current_cities = self.config_entry.options.get(CONF_CITIES, [])

        if user_input is not None:
            cities = user_input.get(CONF_CITIES, [])
            if not cities:
                errors["base"] = "no_cities"
            else:
                removed = [c for c in current_cities if c not in cities]
                if removed:
                    self._pending_cities = cities
                    return await self.async_step_confirm_remove()
                return self.async_create_entry(data={CONF_CITIES: cities})

        schema = vol.Schema(
            {
                vol.Required(CONF_CITIES, default=current_cities): SelectSelector(
                    SelectSelectorConfig(
                        options=CITY_OPTIONS,
                        multiple=True,
                        mode=SelectSelectorMode.LIST,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_confirm_remove(self, user_input=None):
        current_cities = self.config_entry.options.get(CONF_CITIES, [])
        cities = self._pending_cities if self._pending_cities is not None else current_cities
        removed = [c for c in current_cities if c not in cities]
        removed_labels = "\n".join(
            f"- {c} ({CITY_EN_NAMES.get(c, c)})" for c in removed
        )

        if user_input is not None:
            return self.async_create_entry(data={CONF_CITIES: cities})

        return self.async_show_form(
            step_id="confirm_remove",
            data_schema=vol.Schema({}),
            description_placeholders={"cities": removed_labels},
        )
