import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate, sensor, switch, output, text_sensor, binary_sensor
from esphome.const import (
    CONF_ID,
    ENTITY_CATEGORY_DIAGNOSTIC,
)

CODEOWNERS = ["@your_username"]
AUTO_LOAD = ["climate"]

dummy_thermostat_ns = cg.esphome_ns.namespace("dummy_thermostat")
DummyThermostat = dummy_thermostat_ns.class_(
    "DummyThermostat", climate.Climate, cg.Component
)

# Configuration keys
CONF_FALLBACK_SENSOR = "fallback_sensor"
CONF_SENSOR_TIMEOUT = "sensor_timeout"
CONF_FALLBACK_SENSOR_TIMEOUT = "fallback_sensor_timeout"
CONF_FALLBACK_HUMIDITY_SENSOR = "fallback_humidity_sensor"
CONF_HUMIDITY_SENSOR_TIMEOUT = "humidity_sensor_timeout"
CONF_VALVE_UPDATE_TIMEOUT = "valve_update_timeout"
CONF_VALVE_OUTPUT = "valve_output"
CONF_VALVE_SWITCH = "valve_switch"
CONF_VALVE_CONTROL_ENABLED = "valve_control_enabled"
CONF_USE_LOCAL_VALVE_CONTROL = "use_local_valve_control"
CONF_HEATING_DEADBAND = "heating_deadband"
CONF_HEATING_OVERRUN = "heating_overrun"
CONF_COOLING_DEADBAND = "cooling_deadband"
CONF_COOLING_OVERRUN = "cooling_overrun"
CONF_DIAGNOSTIC_SOURCE_STATUS = "diagnostic_source_status"
CONF_DIAGNOSTIC_FALLBACK_TEMPERATURE_ACTIVE = "diagnostic_fallback_temperature_active"
CONF_DIAGNOSTIC_FALLBACK_HUMIDITY_ACTIVE = "diagnostic_fallback_humidity_active"
CONF_DIAGNOSTIC_LOCAL_CONTROLLER_ACTIVE = "diagnostic_local_controller_active"


CONFIG_SCHEMA = climate.climate_schema(DummyThermostat).extend(
    {
        cv.Optional(CONF_FALLBACK_SENSOR): cv.use_id(sensor.Sensor),
        cv.Optional(CONF_SENSOR_TIMEOUT, default=600): cv.positive_int,
        cv.Optional(CONF_FALLBACK_SENSOR_TIMEOUT, default=600): cv.positive_int,
        cv.Optional(CONF_FALLBACK_HUMIDITY_SENSOR): cv.use_id(sensor.Sensor),
        cv.Optional(CONF_HUMIDITY_SENSOR_TIMEOUT, default=0): cv.positive_int,
        cv.Optional(CONF_VALVE_UPDATE_TIMEOUT, default=0): cv.positive_int,
        cv.Optional(CONF_VALVE_OUTPUT): cv.use_id(output.FloatOutput),
        cv.Optional(CONF_VALVE_SWITCH): cv.use_id(switch.Switch),
        cv.Optional(CONF_VALVE_CONTROL_ENABLED, default=False): cv.templatable(cv.boolean),
        cv.Optional(CONF_USE_LOCAL_VALVE_CONTROL, default=False): cv.templatable(cv.boolean),
        cv.Optional(CONF_HEATING_DEADBAND, default=0.5): cv.temperature,
        cv.Optional(CONF_HEATING_OVERRUN, default=0.5): cv.temperature,
        cv.Optional(CONF_COOLING_DEADBAND, default=0.5): cv.temperature,
        cv.Optional(CONF_COOLING_OVERRUN, default=0.5): cv.temperature,
        cv.Optional(CONF_DIAGNOSTIC_SOURCE_STATUS): text_sensor.text_sensor_schema(
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC
        ),
        cv.Optional(CONF_DIAGNOSTIC_FALLBACK_TEMPERATURE_ACTIVE): binary_sensor.binary_sensor_schema(
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC
        ),
        cv.Optional(CONF_DIAGNOSTIC_FALLBACK_HUMIDITY_ACTIVE): binary_sensor.binary_sensor_schema(
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC
        ),
        cv.Optional(CONF_DIAGNOSTIC_LOCAL_CONTROLLER_ACTIVE): binary_sensor.binary_sensor_schema(
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC
        ),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await climate.register_climate(var, config)


    if CONF_FALLBACK_SENSOR in config:
        fallback_sens = await cg.get_variable(config[CONF_FALLBACK_SENSOR])
        cg.add(var.set_fallback_sensor(fallback_sens))

    cg.add(var.set_sensor_timeout(config[CONF_SENSOR_TIMEOUT]))
    cg.add(var.set_fallback_sensor_timeout(config[CONF_FALLBACK_SENSOR_TIMEOUT]))

    if CONF_FALLBACK_HUMIDITY_SENSOR in config:
        fallback_humidity_sens = await cg.get_variable(config[CONF_FALLBACK_HUMIDITY_SENSOR])
        cg.add(var.set_fallback_humidity_sensor(fallback_humidity_sens))

    cg.add(var.set_humidity_sensor_timeout(config[CONF_HUMIDITY_SENSOR_TIMEOUT]))

    cg.add(var.set_valve_update_timeout(config[CONF_VALVE_UPDATE_TIMEOUT]))

    if CONF_VALVE_OUTPUT in config:
        valve_out = await cg.get_variable(config[CONF_VALVE_OUTPUT])
        cg.add(var.set_valve_output(valve_out))

    if CONF_VALVE_SWITCH in config:
        valve_sw = await cg.get_variable(config[CONF_VALVE_SWITCH])
        cg.add(var.set_valve_switch(valve_sw))

    if CONF_VALVE_CONTROL_ENABLED in config:
        template_ = await cg.templatable(config[CONF_VALVE_CONTROL_ENABLED], [], cg.bool_)
        cg.add(var.set_valve_control_enabled(template_))

    if CONF_USE_LOCAL_VALVE_CONTROL in config:
        template_ = await cg.templatable(config[CONF_USE_LOCAL_VALVE_CONTROL], [], cg.bool_)
        cg.add(var.set_use_local_valve_control(template_))

    cg.add(var.set_heating_deadband(config[CONF_HEATING_DEADBAND]))
    cg.add(var.set_heating_overrun(config[CONF_HEATING_OVERRUN]))
    cg.add(var.set_cooling_deadband(config[CONF_COOLING_DEADBAND]))
    cg.add(var.set_cooling_overrun(config[CONF_COOLING_OVERRUN]))

    if CONF_DIAGNOSTIC_SOURCE_STATUS in config:
        diagnostic_status = await text_sensor.new_text_sensor(config[CONF_DIAGNOSTIC_SOURCE_STATUS])
        cg.add(var.set_source_status_text_sensor(diagnostic_status))

    if CONF_DIAGNOSTIC_FALLBACK_TEMPERATURE_ACTIVE in config:
        diagnostic_fallback_temp = await binary_sensor.new_binary_sensor(
            config[CONF_DIAGNOSTIC_FALLBACK_TEMPERATURE_ACTIVE]
        )
        cg.add(var.set_fallback_temperature_binary_sensor(diagnostic_fallback_temp))

    if CONF_DIAGNOSTIC_FALLBACK_HUMIDITY_ACTIVE in config:
        diagnostic_fallback_humidity = await binary_sensor.new_binary_sensor(
            config[CONF_DIAGNOSTIC_FALLBACK_HUMIDITY_ACTIVE]
        )
        cg.add(var.set_fallback_humidity_binary_sensor(diagnostic_fallback_humidity))

    if CONF_DIAGNOSTIC_LOCAL_CONTROLLER_ACTIVE in config:
        diagnostic_local_controller = await binary_sensor.new_binary_sensor(
            config[CONF_DIAGNOSTIC_LOCAL_CONTROLLER_ACTIVE]
        )
        cg.add(var.set_local_controller_binary_sensor(diagnostic_local_controller))
    