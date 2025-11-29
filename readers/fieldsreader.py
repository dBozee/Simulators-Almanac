from pathlib import Path
from xml.etree.ElementTree import Element

from pydantic import ValidationError
from pydantic_xml import BaseXmlModel, attr

from enums import FruitType, GroundType, SprayType

from .base_reader import BaseReader


class FieldsReader(BaseReader):
    def __init__(self, path: Path, owner_id: str = "1"):
        path = path / "fields.xml"
        super().__init__(path)

        self.owner_id = owner_id
        self.all_fields = self.parse_fields()

    def parse_fields(self) -> list[FarmField]:
        fields = self.doc.getroot()
        return [res for field in fields if (res := self._try_parse_one_field(field))]

    @staticmethod
    def _try_parse_one_field(field: Element) -> FarmField | None:
        try:
            return FarmField.from_xml_tree(field)
        except ValidationError as e:
            fld_id = field.get("id", "UNKNOWN")
            print(f"Failed to parse field with ID {fld_id} with error: {e}")


class FarmField(BaseXmlModel, tag="field"):
    class Config:
        @staticmethod
        def to_camel(field_name: str) -> str:
            words = field_name.split("_")
            return words[0] + "".join(word.title() for word in words[1:])

        alias_generator = to_camel

    id: str = attr()
    planned_fruit: str = attr()
    fruit_type: FruitType = attr()
    growth_state: int = attr()
    last_growth_state: int = attr()
    weed_state: int = attr()
    stone_level: int = attr()
    ground_type: GroundType = attr()
    spray_type: SprayType = attr()
    spray_level: int = attr()
    lime_level: int = attr()
    roller_level: int = attr()
    plow_level: int = attr()
    stubble_shred_level: int = attr()
    water_level: int = attr()
