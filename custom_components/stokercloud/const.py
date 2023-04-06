from homeassistant.const import CONF_USERNAME
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

DOMAIN = "stokercloud"
DATA_SCHEMA = vol.Schema({vol.Required(CONF_USERNAME): cv.string})
PLATFORMS = ['sensor', 'water_heater']