from pathlib import Path
from xml.etree.ElementTree import Element

from pydantic import ValidationError

from readers import BaseReader
from readers.base_reader import ConfiguredXmlModel


class Farmland(BaseReader):
    def __init__(self, path: Path):
        super().__init__(path)

        self.farmlands: list[FarmlandModel] = self._parse_farmlands()

    def _parse_farmlands(self):
        farmlands = self.doc.getroot()
        return [
            res
            for farmland in farmlands
            if (res := FarmlandModel.from_xml_tree(farmland))
        ]

    @staticmethod
    def _try_parse_one_farmland(farmland: Element) -> FarmlandModel | None:
        try:
            return FarmlandModel.from_xml_tree(farmland)
        except ValidationError as e:
            fld_id = farmland.get("id", "UNKNOWN")
            print(f"Failed to parse farmland with ID {fld_id} with error: {e}")

    def owned_farmlands(self, owner_id: str) -> list[FarmlandModel]:
        return [farm for farm in self.farmlands if owner_id == farm.farm_id]


class FarmlandModel(ConfiguredXmlModel, tag="farmland"):
    id: str
    farm_id: str
    npc_index: str
