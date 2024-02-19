from abc import ABC, abstractmethod


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
