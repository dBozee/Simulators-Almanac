from functools import cached_property
from logging import getLogger

from .base_reader import BaseReader
from .environment import Environment, EnvironmentReader
from .farmland import Farmland, FarmlandReader
from .farms import Farm, FarmsReader
from .fields import FarmField, FieldsReader

log = getLogger(__name__)


class AllReaders:
    def __init__(self, path, farm_id: str = 1):
        self.farm_id = farm_id
        self.path = path
        self._fields_reader: FieldsReader | None = self._model_factory(FieldsReader)
        self._environment_reader: EnvironmentReader | None = self._model_factory(EnvironmentReader)
        self._farmland_reader: FarmlandReader | None = self._model_factory(FarmlandReader)
        self._farms_reader: FarmsReader | None = self._model_factory(FarmsReader)

    @cached_property
    def fields(self) -> list[FarmField]:
        return self._fields_reader.all_fields if self._fields_reader else []

    @cached_property
    def owned_fields(self) -> list[FarmField]:
        if not (all_fields := self.fields):
            return []
        owned_farm_ids = [farm.id for farm in self.owned_farmlands]
        return [field for field in all_fields if field.id in owned_farm_ids]

    @cached_property
    def environment(self) -> Environment | None:
        return self._environment_reader.environment if self._environment_reader else None

    @cached_property
    def farmlands(self) -> list[Farmland]:
        return self._farmland_reader.farmlands if self._farmland_reader else []

    @cached_property
    def owned_farmlands(self):
        return self._farmland_reader.owned_farmlands(self.farm_id) if self._farmland_reader else []

    @cached_property
    def farms(self) -> list[Farm]:
        return self._farms_reader.farms if self._farms_reader else []

    @cached_property
    def my_farm(self) -> Farm | None:
        return next((farm for farm in self.farms if farm.farm_id == self.farm_id), None)

    def farm_by_id(self, farm_id: int) -> Farm | None:
        return next((farm for farm in self.farms if farm.farm_id == farm_id), None)

    def _model_factory(self, model: type[BaseReader]):
        try:
            return model(path=self.path)
        except Exception as e:
            log.warning(f"Failed to instantiate {model.__name__} with error: {e}")
            return None
