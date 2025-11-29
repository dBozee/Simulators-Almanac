from pathlib import Path
from typing import Annotated

from pydantic_xml import attr

from enums import FruitType, GroundType, SprayType

from .base_reader import BaseReader, ConfiguredXmlModel


class FieldsReader(BaseReader):
    def __init__(self, path: Path):
        path = path / "fields.xml"
        super().__init__(path)

        self.all_fields: list[FarmField] = self._parse_all(FarmField)


class FarmField(ConfiguredXmlModel, tag="field"):
    id: Annotated[str, attr()]
    planned_fruit: Annotated[str, attr()]
    fruit_type: Annotated[FruitType, attr()]
    growth_state: Annotated[int, attr()]
    last_growth_state: Annotated[int, attr()]
    weed_state: Annotated[int, attr()]
    stone_level: Annotated[int, attr()]
    ground_type: Annotated[GroundType, attr()]
    spray_type: Annotated[SprayType, attr()]
    spray_level: Annotated[int, attr()]
    lime_level: Annotated[int, attr()]
    roller_level: Annotated[int, attr()]
    plow_level: Annotated[int, attr()]
    stubble_shred_level: Annotated[int, attr()]
    water_level: Annotated[int, attr()]
