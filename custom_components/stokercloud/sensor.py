"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.const import STATE_OFF, STATE_ON

from stokercloud.controller_data import PowerState, Unit, Value
from stokercloud.client import Client as StokerCloudClient


import datetime
from homeassistant.const import CONF_USERNAME, POWER_KILO_WATT, TEMP_CELSIUS, MASS_KILOGRAMS, MASS_GRAMS, PERCENTAGE, PRESSURE_PA, VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR
from .const import DOMAIN
from .mixins import StokerCloudControllerMixin

import logging

logger = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(minutes=1)

async def async_setup_entry(hass, config, async_add_entities):
    """Set up the sensor platform."""
    client = hass.data[DOMAIN][config.entry_id]
    serial = config.data[CONF_USERNAME]
    async_add_entities([
        StokerCloudControllerBinarySensor(client, serial, 'Running', 'running', 'power'),
        StokerCloudControllerBinarySensor(client, serial, 'Alarm', 'alarm', 'problem'),
        StokerCloudControllerSensor(client, serial, 'Boiler Temperature', 'boiler_temperature_current', SensorDeviceClass.TEMPERATURE),
        StokerCloudControllerSensor(client, serial, 'Boiler Temperature Requested', 'boiler_temperature_requested', SensorDeviceClass.TEMPERATURE),
        StokerCloudControllerSensor(client, serial, 'Boiler Return Temperature', 'boiler_temp_return', SensorDeviceClass.TEMPERATURE),         
        StokerCloudControllerSensor(client, serial, 'Boiler Dropshaft Temperature', 'boiler_temp_dropshaft', SensorDeviceClass.TEMPERATURE),
        StokerCloudControllerSensor(client, serial, 'HotWater Temperature', 'hotwater_temperature_current', SensorDeviceClass.TEMPERATURE),         
        StokerCloudControllerSensor(client, serial, 'HotWater Temperature Requested', 'hotwater_temperature_requested', SensorDeviceClass.TEMPERATURE),
        StokerCloudControllerSensor(client, serial, 'Boiler Power', 'boiler_kwh', SensorDeviceClass.POWER),
        StokerCloudControllerSensor(client, serial, 'Total Consumption', 'consumption_total', state_class=SensorStateClass.TOTAL_INCREASING), # state class STATE_CLASS_TOTAL_INCREASING
        StokerCloudControllerSensor(client, serial, 'Consumption 24h', 'consumption_day', state_class=SensorStateClass.TOTAL_INCREASING), # 
        StokerCloudControllerSensor(client, serial, 'State', 'state'),
        StokerCloudControllerSensor(client, serial, 'State_pom', 'state_pom'),                                                                          
        StokerCloudControllerSensor(client, serial, 'O2 reference', 'oxygen_reference'),                                                                          
        StokerCloudControllerSensor(client, serial, 'Airflow', 'airflow'),                                                                          
        StokerCloudControllerSensor(client, serial, 'Boliler Power Output', 'boiler_percent', SensorDeviceClass.POWER_FACTOR),
        StokerCloudControllerSensor(client, serial, 'Chimney/Smoke Temp', 'smoke_temperature', SensorDeviceClass.TEMPERATURE),
        StokerCloudControllerSensor(client, serial, 'O2', 'oxygen_current', SensorDeviceClass.POWER_FACTOR),
        StokerCloudControllerSensor(client, serial, 'O2 low regulation', 'oxygen_low', SensorDeviceClass.POWER_FACTOR),
        StokerCloudControllerSensor(client, serial, 'O2 mid regulation', 'oxygen_mid', SensorDeviceClass.POWER_FACTOR),
        StokerCloudControllerSensor(client, serial, 'O2 high regulation', 'oxygen_high', SensorDeviceClass.POWER_FACTOR),
        StokerCloudControllerSensor(client, serial, 'Auger capacity', 'auger_capacity', SensorDeviceClass.WEIGHT),
        StokerCloudControllerSensor(client, serial, 'Power 10%', 'power_10_percent', SensorDeviceClass.POWER),                         
        StokerCloudControllerSensor(client, serial, 'Power 100%', 'power_100_percent', SensorDeviceClass.POWER),                         
        StokerCloudControllerSensor(client, serial, 'DHW-Difference under', 'dhw_difference_under', SensorDeviceClass.TEMPERATURE),                         
        StokerCloudControllerSensor(client, serial, 'Hopper distance', 'hopper_distance'),                             
        StokerCloudControllerSensor(client, serial, 'Ash Distance', 'ashdist'),                             
        StokerCloudControllerSensor(client, serial, 'Hopper distance max', 'hopper_distance_max'),                                                                        
        StokerCloudControllerSensor(client, serial, 'DHW Pump', 'dhw_pump'),                             
        StokerCloudControllerSensor(client, serial, 'Boiler Pump', 'boiler_pump'),                             
        StokerCloudControllerSensor(client, serial, 'Weather Zone 1 Valve position', 'weather_zone1_valve_position'),                               
        StokerCloudControllerSensor(client, serial, 'Weather Pump', 'weather_pump'),                               
        StokerCloudControllerSensor(client, serial, 'Exhaust fan', 'exhaust_fan'),                               
        StokerCloudControllerSensor(client, serial, 'Output6', 'l_6'),                               
        StokerCloudControllerSensor(client, serial, 'Compressor cleaning', 'compressor_cleaning', SensorDeviceClass.WEIGHT),                               
        StokerCloudControllerSensor(client, serial, 'Output8', 'l_8'),                               
        StokerCloudControllerSensor(client, serial, 'Weather Pump2', 'weather_pump2'),                               
        StokerCloudControllerSensor(client, serial, 'Weather: Zone 1', 'weather_zone1_active'),                               
        StokerCloudControllerSensor(client, serial, 'Weather: Zone 2', 'weather_zone2_active'),                               
        StokerCloudControllerSensor(client, serial, 'Zone 1: Wanted flow', 'zone1_flow_wanted', SensorDeviceClass.TEMPERATURE),                           
        StokerCloudControllerSensor(client, serial, 'Zone 1: Actual flow', 'zone1_flow_current', SensorDeviceClass.TEMPERATURE),                           
        StokerCloudControllerSensor(client, serial, 'Zone 1: Valve Position', 'zone1_valve_position'),             
        StokerCloudControllerSensor(client, serial, 'Zone 1: Current Temperature.', 'zone1_current_temperature', SensorDeviceClass.TEMPERATURE),             
        StokerCloudControllerSensor(client, serial, 'Zone 1: Avarage Temperature.', 'zone1_avarage_temperature', SensorDeviceClass.TEMPERATURE),             
        StokerCloudControllerSensor(client, serial, 'Zone 2: Wanted flow', 'zone2_flow_wanted', SensorDeviceClass.TEMPERATURE),        
        StokerCloudControllerSensor(client, serial, 'Zone 2: Actual flow', 'zone2_flow_current', SensorDeviceClass.TEMPERATURE),      
        StokerCloudControllerSensor(client, serial, 'Zone 2: Valve Position', 'zone2_valve_position'),                  
        StokerCloudControllerSensor(client, serial, 'Zone 2: Current Temperature', 'zone2_current_temperature', SensorDeviceClass.TEMPERATURE),              
        StokerCloudControllerSensor(client, serial, 'Zone 2: Avarage Temperature', 'zone2_avarage_temperature', SensorDeviceClass.TEMPERATURE),            
        StokerCloudControllerSensor(client, serial, 'Hopper Content', 'hopper_content', SensorDeviceClass.WEIGHT),        
        StokerCloudControllerSensor(client, serial, 'Hopper Trip1', 'hopper_trip1', SensorDeviceClass.WEIGHT),                                                             
        StokerCloudControllerSensor(client, serial, 'Hopper Trip2', 'hopper_trip2', SensorDeviceClass.WEIGHT),                                                               
        StokerCloudControllerSensor(client, serial, 'Pressure', 'pressure', SensorDeviceClass.PRESSURE),          
    ])
                                                                                                                           

class StokerCloudControllerBinarySensor(StokerCloudControllerMixin, BinarySensorEntity):
    """Representation of a Sensor."""

    def __init__(self, client: StokerCloudClient, serial, name: str, client_key: str, device_class):
        """Initialize the sensor."""
        super(StokerCloudControllerBinarySensor, self).__init__(client, serial, name, client_key)
        self._device_class = device_class

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._state is PowerState.on

    @property
    def device_class(self):
        return self._device_class


class StokerCloudControllerSensor(StokerCloudControllerMixin, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, client: StokerCloudClient, serial, name: str, client_key: str, device_class=None, state_class=None):
        """Initialize the sensor."""
        super(StokerCloudControllerSensor, self).__init__(client, serial, name, client_key)
        self._device_class = device_class
        self._attr_state_class = state_class

    @property
    def device_class(self):
        return self._device_class

    @property
    def native_value(self):
        """Return the value reported by the sensor."""
        if self._state:
            if isinstance(self._state, Value):
                return self._state.value
            return self._state

    @property
    def native_unit_of_measurement(self):
        if self._state and isinstance(self._state, Value):
            return {
                Unit.KWH: POWER_KILO_WATT,
                Unit.DEGREE: TEMP_CELSIUS,
                Unit.KILO_GRAM: MASS_KILOGRAMS,
                Unit.GRAM: MASS_GRAMS,
                Unit.PERCENT: PERCENTAGE,
                Unit.PASCAL: PRESSURE_PA,
				Unit.M3H: VOLUME_FLOW_RATE_CUBIC_METERS_PER_HOUR,
            }.get(self._state.unit)

