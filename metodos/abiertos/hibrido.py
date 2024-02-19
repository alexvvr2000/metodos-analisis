from collections.abc import Iterable
from dataclasses import dataclass

from metodos.abiertos.newton import Newton
from metodos.tipos import Funcion2d, IteracionABC


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


class Hibrido:
    iteracion_actual: int
    iteracion_maxima: int
    funcion: Funcion2d
    derivada: Funcion2d
    fila_anterior: IteracionABC
    a_inicial: float
    b_inicial: float

    def __init__(
        self,
        funcion: Funcion2d,
        derivada: Funcion2d,
        a_inicial: float,
        b_inicial: float,
        iteracion_maxima: int,
    ) -> None:
        if not b_inicial > a_inicial:
            raise Exception("Rango inicial debe ser [a,b] donde b > a")

        self.funcion = funcion
        self.derivada = derivada
        self.iteracion_maxima = iteracion_maxima
        self.a_inicial = a_inicial
        self.b_inicial = b_inicial
