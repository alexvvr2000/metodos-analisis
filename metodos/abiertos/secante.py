from dataclasses import dataclass

from metodos.tipos import Funcion2d, IteracionABC


@dataclass
class IteracionSecante(IteracionABC):
    iteracion: int
    x_i_anterior: float
    x_i_actual: float
    x_i_siguiente: float
    error_relativo: float

    def obtener_x_i(self) -> float:
        return self.x_i_siguiente

    def obtener_iteracion(self) -> int:
        return self.iteracion

    def obtener_error_relativo(self) -> float:
        return self.error_relativo


class Secante:
    valor_inicial: float
    funcion: Funcion2d
    fila_actual: IteracionSecante
    iteracion_actual: int
    iteracion_maxima: int

    def __init__(
        self,
        valor_inicial: int,
        funcion: Funcion2d,
        iteracion_maxima: int,
    ) -> None:
        if iteracion_maxima <= 0:
            raise Exception("Debe ser 1 o mas iteraciones")

        self.valor_inicial = valor_inicial
        self.funcion = funcion
        self.iteracion_maxima = iteracion_maxima

    def __iter__(self):
        return self

    def get_error_relativo(self, r_actual: float, r_anterior: float) -> float:
        return abs((r_actual - r_anterior) / r_actual)
