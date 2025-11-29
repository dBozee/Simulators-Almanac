from pathlib import Path
from xml.etree.ElementTree import ElementTree

from defusedxml.ElementTree import parse
from pydantic_xml import BaseXmlModel


class BaseReader:
    def __init__(self, path: Path):
        self.path: Path = path
        self.doc: ElementTree | None = parse(str(path))


class ConfiguredXmlModel(BaseXmlModel):
    class Config:
        extra = "allow"

        @staticmethod
        def to_camel(field_name: str) -> str:
            words = field_name.split("_")
            return words[0] + "".join(word.title() for word in words[1:])

        alias_generator = to_camel
