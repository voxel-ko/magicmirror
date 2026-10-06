import json
import os
import re

from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Config:
    latitude: int
    longitude: int
    timezone: str
    speed_unit: str
    temperature_unit: str
    max_events_per_day: int


config: Config = Config(
    latitude=0,
    longitude=0,
    timezone="UTC",
    speed_unit="kmh",
    temperature_unit="celsius",
    max_events_per_day=3
)

def create_default_config():
    config_json = json.dumps(config.__dict__, indent=4)

    directory_path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(directory_path, "config.json"), "w") as file:
        file.write(config_json)

def grab_geolocation_data(json_data):
    from . import weather_data

    if json_data.get("latitude") == "auto":
        latitude, _, _ = weather_data.get_geolocation()
    else:
        latitude = json_data.get("latitude")

    assert latitude is not None

    if json_data.get("longitude") == "auto":
        _, longitude, _ = weather_data.get_geolocation()
    else:
        longitude = json_data.get("longitude")

    assert longitude is not None

    if json_data.get("timezone") == "auto":
        _, _, timezone = weather_data.get_geolocation()
    else:
        timezone = json_data.get("timezone")

    assert timezone is not None

    return latitude, longitude, timezone

def get_config_option(user_config, option, regex=None):
    user_option = user_config.get(option)
    default_option = getattr(config, option)

    if regex is None:
        return user_option or default_option

    match = re.match(regex, str(user_option))
    # I have no clue why it won't just let me do `if match` to check if there's an actual match
    if match and sum(match.span()) != 0:
        group_dict = match.groupdict()

        value = next(filter(
            lambda group: group_dict[group] is not None,
            group_dict
        ))
    else:
        logger.warning("Could not find value for %s in config, falling back to default",
                                    str(option), exc_info=True)
        value = default_option

    return value

def init(root_path):
    global config

    directory_path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(os.path.join(directory_path, "config.json")):
        logger.warning("config.json file does not exist, creating default one")
        create_default_config()

    with open(os.path.join(root_path, "config.json"), "r") as f:
        file_contents = f.read()

    json_data = json.loads(file_contents)

    latitude, longitude, timezone = grab_geolocation_data(json_data)

    config = Config(
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        speed_unit=get_config_option(json_data, "speed_unit",
     r"(?P<kmh>^(kmh)?(kilometers)?$)?(?P<ms>^(ms)(miles)?$)?"),
        temperature_unit=get_config_option(json_data, "temperature_unit",
    r"(?P<fahrenheit>^(f)(ah)?(renheit)?$)?(?P<celsius>^(c)(el)?(sius)?$)?"),
        max_events_per_day=int(get_config_option(json_data, "max_events_per_day"))
    )


if __name__ == "__main__":
    if input("Override config.json with defaults? (y/N) ").lower() != "y":
        exit()

    create_default_config()
