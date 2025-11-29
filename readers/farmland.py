from pathlib import Path

from pydantic_xml import attr

from .base_reader import BaseReader, ConfiguredXmlModel


class FarmlandReader(BaseReader):
    def __init__(self, path: Path):
        path = path / "farmland.xml"
        super().__init__(path)

        self.farmlands: list[Farmland] = self._parse_all(Farmland)

    def owned_farmlands(self, farm_id: str) -> list[Farmland]:
        return [farm for farm in self.farmlands if farm_id == farm.farm_id]


class Farmland(ConfiguredXmlModel, tag="farmland"):
    id: str = attr()
    farm_id: str = attr()
    npc_index: str | None = attr(default=None)
