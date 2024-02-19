from dataclasses import dataclass

from metodos.tipos import Funcion2d, IteracionABC
from metodos.utils import get_error_relativo


@dataclass
class IteracionSecante(IteracionABC):
    iteracion: int
    xi_anterior: float
    xi_actual: float
    xi_siguiente: float
    error_relativo: float

    def obtener_x_i(self) -> float:
        return self.xi_siguiente

    def obtener_iteracion(self) -> int:
        return self.iteracion

    def obtener_error_relativo(self) -> float:
        return self.error_relativo


class Secante:
    xi_anterior_inicial: float
    xi_inicial: float
    funcion: Funcion2d
    fila_anterior: IteracionSecante
    iteracion_actual: int = 0
    iteracion_maxima: int

    def __init__(
        self,
        xi_anterior_inicial: float,
        xi_inicial: float,
        funcion: Funcion2d,
        iteracion_maxima: int,
    ) -> None:
        if iteracion_maxima <= 0:
            raise Exception("Debe ser 1 o mas iteraciones")

        self.xi_anterior_inicial = xi_anterior_inicial
        self.xi_inicial = xi_inicial
        self.funcion = funcion
        self.iteracion_maxima = iteracion_maxima

    def __iter__(self):
        return self

    @staticmethod
    def obtener_x_siguiente(
        funcion: Funcion2d, xi_actual: float, xi_anterior: float
    ) -> float:
        return xi_actual - (funcion(xi_actual) * (xi_anterior - xi_actual)) / (
            funcion(xi_anterior) - funcion(xi_actual)
        )

    def __next__(self) -> IteracionSecante:
        if self.iteracion_actual == self.iteracion_maxima:
            raise StopIteration
        self.iteracion_actual += 1
        xi_anterior: float
        xi_actual: float
        xi_siguiente: float
        if self.iteracion_actual == 1:
            xi_anterior = self.xi_anterior_inicial
            xi_actual = self.xi_inicial
        else:
            xi_anterior = self.fila_anterior.xi_actual
            xi_actual = self.fila_anterior.xi_siguiente
        xi_siguiente = self.obtener_x_siguiente(self.funcion, xi_actual, xi_anterior)
        error_relativo: float = (
            -1
            if self.iteracion_actual == 1
            else get_error_relativo(xi_siguiente, self.fila_anterior.xi_siguiente)
        )
        self.fila_anterior = IteracionSecante(
            iteracion=self.iteracion_actual,
            xi_anterior=xi_anterior,
            xi_actual=xi_actual,
            xi_siguiente=xi_siguiente,
            error_relativo=error_relativo,
        )
        return self.fila_anterior


if __name__ == "__main__":
    from math import exp

    def funcion(x: float) -> float:
        return exp(-x) - x

    for iteracion in Secante(0, 1, funcion, 4):
        print(iteracion, "\n")
