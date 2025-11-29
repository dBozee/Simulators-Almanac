from pathlib import Path
from typing import Annotated

from pydantic import ValidationError
from pydantic_xml import attr, element

from enums import Season, WeatherType

from .base_reader import BaseReader, ConfiguredXmlModel


class EnvironmentReader(BaseReader):
    def __init__(self, path: Path):
        path = path / "environment.xml"
        super().__init__(path)
        self.environment: Environment | None

        try:
            self.environment = Environment.from_xml_tree(self.doc.getroot())
        except ValidationError as e:
            print(f"Failed to load Environment from {self.path} with error: {e}")
            self.environment = None


class SnowRoot(ConfiguredXmlModel, tag="snow"):
    height: Annotated[float, attr()]
    physical_height: Annotated[float, attr()]


class Snow(ConfiguredXmlModel, tag="snow"):
    height: Annotated[float, attr()]


class Ground(ConfiguredXmlModel, tag="ground"):
    wetness: Annotated[float, attr()]


class Twister(ConfiguredXmlModel, tag="twister"):
    position: Annotated[str, attr()]
    is_spawned: Annotated[bool, attr()]


class Instance(ConfiguredXmlModel, tag="instance"):
    type_name: Annotated[WeatherType, attr()]
    season: Annotated[Season, attr()]
    variation_index: Annotated[int, attr()]
    start_day: Annotated[int, attr()]
    start_day_time: Annotated[int, attr()]
    duration: Annotated[int, attr()]


class Forecast(ConfiguredXmlModel):
    instances: Annotated[list[Instance], element(default_factory=list, tag="instance")]


class ToneMapping(ConfiguredXmlModel, tag="toneMapping"):
    slope: Annotated[float, attr()]
    toe: Annotated[float, attr()]
    shoulder: Annotated[float, attr()]
    black_clip: Annotated[float, attr()]
    white_clip: Annotated[float, attr()]


class Lighting(ConfiguredXmlModel, tag="lighting"):
    tone_mapping: Annotated[ToneMapping, element()]


class GroundFog(ConfiguredXmlModel, tag="groundFog"):
    coverage_edge0: Annotated[float, attr()]
    coverage_edge1: Annotated[float, attr()]
    extra_height: Annotated[float, attr()]
    ground_level_density: Annotated[float, attr()]
    min_valley_depth: Annotated[float, attr()]
    start_day_time_minutes: Annotated[int, attr()]
    end_day_time_minutes: Annotated[int, attr()]
    weather_types: Annotated[str | None, attr(default=None)]


class HeightFog(ConfiguredXmlModel, tag="heightFog"):
    max_height: Annotated[float, attr()]
    ground_level_density: Annotated[float, attr()]


class FogData(ConfiguredXmlModel):
    ground_fog: Annotated[GroundFog, element()]
    height_fog: Annotated[HeightFog, element()]


class Fog(ConfiguredXmlModel, tag="fog"):
    alpha: Annotated[float, attr()]
    visibility_alpha: Annotated[float, attr()]
    target: Annotated[FogData, element(tag="target")]
    last: Annotated[FogData, element(tag="last")]


class Weather(ConfiguredXmlModel):
    time_since_last_rain: Annotated[int, attr()]
    forecast: Annotated[Forecast, element()]
    fog: Annotated[Fog, element()]
    snow: Annotated[Snow, element()]
    ground: Annotated[Ground, element()]
    twister: Annotated[Twister, element()]


class Environment(ConfiguredXmlModel, tag="environment"):
    day_time: Annotated[float, element()]
    current_day: Annotated[int, element()]
    current_monotonic_day: Annotated[int, element()]
    real_hour_timer: Annotated[int, element()]
    days_per_period: Annotated[int, element()]
    lighting: Annotated[Lighting, element()]
    weather: Annotated[Weather, element()]
    snow: Annotated[SnowRoot, element()]
