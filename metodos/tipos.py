from abc import ABC, abstractmethod
from collections.abc import Callable


class IteracionABC(ABC):
    @abstractmethod
    def obtener_iteracion(self) -> int:
        pass

    @abstractmethod
    def obtener_x_i(self) -> float:
        pass

    @abstractmethod
    def obtener_error_relativo(self) -> float:
        pass


Funcion2d = Callable[[float], float]
