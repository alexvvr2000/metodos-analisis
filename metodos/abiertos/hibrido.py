from dataclasses import dataclass

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
    fila_anterior: IteracionHibrido
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

    def __iter__(self):
        return self

    def __next__(self) -> IteracionHibrido:
        if self.iteracion_actual == self.iteracion_maxima:
            raise StopIteration
        self.iteracion_actual += 1
        return self.fila_anterior
