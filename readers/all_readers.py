from readers import BaseReader
from readers.environmentdata import EnvironmentData
from readers.farmland import Farmland
from readers.fields import Fields


class AllReaders:
    def __init__(self, path):
        self.path = path
        fields: Fields | None = self._model_factory(Fields)
        environment: EnvironmentData | None = self._model_factory(EnvironmentData)
        farmland: Farmland | None = self._model_factory(Farmland)

    def _model_factory(self, model: type[BaseReader]):
        try:
            return model(path=self.path)
        except Exception as e:
            print(f"Failed to instantiate {model.__name__} with error: {e}")
            return None