from pathlib import Path
from xml.etree.ElementTree import Element

from pydantic import ValidationError
from pydantic_xml import attr

from .base_reader import BaseReader, ConfiguredXmlModel


class FarmlandReader(BaseReader):
    def __init__(self, path: Path):
        path = path / "farmland.xml"
        super().__init__(path)

        self.farmlands: list[Farmland] = self._parse_farmlands()

    def _parse_farmlands(self) -> list[Farmland]:
        farmlands = self.doc.getroot()
        return [res for farmland in farmlands if (res := Farmland.from_xml_tree(farmland))]

    @staticmethod
    def _try_parse_one_farmland(farmland: Element) -> Farmland | None:
        try:
            return Farmland.from_xml_tree(farmland)
        except ValidationError as e:
            fld_id = farmland.get("id", "UNKNOWN")
            print(f"Failed to parse farmland with ID {fld_id} with error: {e}")

    def owned_farmlands(self, farm_id: str) -> list[Farmland]:
        return [farm for farm in self.farmlands if farm_id == farm.farm_id]


class Farmland(ConfiguredXmlModel, tag="farmland"):
    id: str = attr()
    farm_id: str = attr()
    npc_index: str | None = attr(default=None)
