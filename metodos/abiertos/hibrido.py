from dataclasses import dataclass

from metodos.tipos import IteracionABC


@dataclass
class IteracionHibrido(IteracionABC):
    iteracion: int
    xi_siguiente: float
    error_relativo: float

    def obtener_x_i(self) -> float:
        return self.xi_siguiente

    def obtener_iteracion(self) -> int:
        return self.iteracion

    def obtener_error_relativo(self) -> float:
        return self.error_relativo
