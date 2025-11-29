from .base_reader import BaseReader
from .environmentreader import Environment, EnvironmentReader
from .farmlandreader import Farmland, FarmlandReader
from .fieldsreader import FarmField, FieldsReader


class AllReaders:
    def __init__(self, path, farm_id: str = 1):
        self.farm_id = farm_id
        self.path = path
        self._fields_reader: FieldsReader | None = self._model_factory(FieldsReader)
        self._environment_reader: EnvironmentReader | None = self._model_factory(EnvironmentReader)
        self._farmland_reader: FarmlandReader | None = self._model_factory(FarmlandReader)

    @property
    def fields(self) -> list[FarmField]:
        return self._fields_reader.all_fields if self._fields_reader else []

    @property
    def environment(self) -> Environment | None:
        return self._environment_reader.environment if self._environment_reader else None

    @property
    def farmlands(self) -> list[Farmland]:
        return self._farmland_reader.farmlands if self._farmland_reader else []

    @property
    def owned_farmlands(self):
        return self._farmland_reader.owned_farmlands(self.farm_id) if self._farmland_reader else []

    def _model_factory(self, model: type[BaseReader]):
        try:
            return model(path=self.path)
        except Exception as e:
            print(f"Failed to instantiate {model.__name__} with error: {e}")
            return None
