from abc import ABC


class IteracionABC(ABC):
    @property
    def iteracion(self) -> int:
        pass

    @property
    def x_i(self) -> float:
        pass

    @property
    def criterio(self) -> float:
        pass

    @property
    def error_relativo(self) -> float:
        pass
