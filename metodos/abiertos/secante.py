from dataclasses import dataclass

from metodos.tipos import Funcion2d, IteracionABC


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
    x0_inicial: float
    x1_inicial: float
    funcion: Funcion2d
    fila_actual: IteracionSecante
    iteracion_actual: int
    iteracion_maxima: int
    primero_calculado: bool = False

    def __init__(
        self,
        x1_inicial: float,
        x0_inicial: float,
        funcion: Funcion2d,
        iteracion_maxima: int,
    ) -> None:
        if iteracion_maxima <= 0:
            raise Exception("Debe ser 1 o mas iteraciones")

        self.x0_inicial = x0_inicial
        self.funcion = funcion
        self.iteracion_maxima = iteracion_maxima
        self.x1_inicial = x1_inicial

    def __iter__(self):
        return self

    def obtener_x_siguiente(self, xi_actual: float, xi_anterior: float) -> float:
        return xi_actual - (self.funcion(xi_actual) * (xi_anterior - xi_actual)) / (
            self.funcion(xi_anterior) - self.funcion(xi_actual)
        )

    def __next__(self) -> IteracionSecante:
        if self.iteracion_actual == self.iteracion_maxima:
            raise StopIteration
        self.iteracion_actual += 1
        self.primero_calculado = True
        return self.fila_actual


if __name__ == "__main__":
    from math import exp

    def funcion(x: float) -> float:
        return exp(-x) - x

    for iteracion in Secante(0, 1, funcion, 4):
        print(iteracion, "\n")
