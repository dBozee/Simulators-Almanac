from logging import getLogger
from pathlib import Path
from typing import TypeVar
from xml.etree.ElementTree import Element, ElementTree

from defusedxml.ElementTree import parse
from pydantic import ValidationError
from pydantic_xml import BaseXmlModel

T = TypeVar("T", bound="ConfiguredXmlModel")

log = getLogger(__name__)


class BaseReader:
    def __init__(self, path: Path):
        self.path: Path = path
        self.doc: ElementTree | None = parse(str(path))

    def _parse_all(self, model: type[ConfiguredXmlModel]) -> list[T]:
        xml_trees = self.doc.getroot()
        return [res for ele in xml_trees if (res := self._parse_one(model, ele))]

    @staticmethod
    def _parse_one(model: type[ConfiguredXmlModel], ele: Element) -> ConfiguredXmlModel | None:
        try:
            return model.from_xml_tree(ele)
        except ValidationError as e:
            fld_id = ele.get("id", "UNKNOWN")
            log.warning(f"Failed to parse field with ID {fld_id} with errors: {e.errors()}")


class ConfiguredXmlModel(BaseXmlModel):
    class Config:
        extra = "allow"

        @staticmethod
        def to_camel(field_name: str) -> str:
            words = field_name.split("_")
            return words[0] + "".join(word.title() for word in words[1:])

        alias_generator = to_camel
