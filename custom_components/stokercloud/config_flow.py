"""Config flow to configure stokercloud.dk integration."""

import voluptuous as vol

from .const import DOMAIN
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME

import logging

_LOGGER = logging.getLogger(__name__)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                username = user_input[CONF_USERNAME]
                info = f"Stoker Cloud: {username}"
                return self.async_create_entry(title=info, data=user_input)
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"

            return self._show_config_form(user_input=user_input, errors=errors)
      
        return self._show_config_form(
            user_input={
#              CONF_NAME: DEFAULT_DEVICE_NAME,
              CONF_USERNAME: "",
#              CONF_PASSWORD: DEFAULT_USERNAME,
            },
            errors=errors,
        )

    # ---------------------------
    #   _show_config_form
    # ---------------------------
    def _show_config_form(self, user_input, errors=None):
        """Show the configuration form to edit data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
#                    vol.Required(CONF_NAME, default=user_input[CONF_NAME]): str,
                    vol.Required(CONF_USERNAME, default=user_input[CONF_USERNAME]): str,
#                    vol.Required(CONF_PASSWORD, default=user_input[CONF_PASSWORD]): str,
                }
            ),
            errors=errors,
        )
