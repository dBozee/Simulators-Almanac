from pathlib import Path
from typing import Annotated

from pydantic import Field, ValidationError
from pydantic_xml import attr

from enums import Season, WeatherType

from .base_reader import BaseReader, ConfiguredXmlModel


class EnvironmentData(BaseReader):
    def __init__(self, path: Path):
        path = path / "environment.xml"
        super().__init__(path)
        self.environment: Environment | None

        try:
            self.environment = Environment.from_xml_tree(self.doc.getroot())
        except ValidationError as e:
            print(f"Failed to load Environment from {self.path} with error: {e}")
            self.environment = None


class Snow(ConfiguredXmlModel, tag="snow"):
    height: float = attr()
    physical_height: float | None = attr()


class Ground(ConfiguredXmlModel, tag="ground"):
    wetness: float = attr()


class Twister(ConfiguredXmlModel, tag="twister"):
    position: str = attr()
    is_spawned: bool = attr()


class Instance(ConfiguredXmlModel, tag="instance"):
    type_name: WeatherType = attr()
    season: Season = attr()
    variation_index: int = attr()
    start_day: int = attr()
    stary_day_time: int = attr()
    duration: int = attr()


class Forecast(ConfiguredXmlModel):
    time_since_last_rain: int
    instances: Annotated[list[Instance], Field(default_factory=list)]


class Weather(ConfiguredXmlModel):
    forecast: Annotated[list[Forecast], Field(default_factory=list)]
    snow: Snow
    ground: Ground
    twister: Twister


class Environment(ConfiguredXmlModel, tag="environment"):
    day_time: int
    current_day: int
    current_monotonic_day: int
    real_hour_timer: int
    days_per_period: int
    weather: Weather
