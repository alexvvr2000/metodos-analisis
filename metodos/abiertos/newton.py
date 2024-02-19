from dataclasses import dataclass
from math import exp
from typing import Callable

from metodos.tipos import Funcion2d, IteracionABC
from metodos.utils import get_error_relativo


@dataclass
class IteracionNewton(IteracionABC):
    x_i: float
    f_x: float
    f_derivada_x: float
    criterio: float
    error_relativo: float
    iteracion: int

    def obtener_x_i(self) -> float:
        return self.x_i

    def obtener_iteracion(self) -> int:
        return self.iteracion

    def obtener_error_relativo(self) -> float:
        return self.error_relativo


class Newton:
    funcion: Funcion2d
    derivada_funcion: Funcion2d
    filaActual: IteracionNewton
    error_relativo: float = -1
    calculado: bool = False
    x_anterior: float
    iteracion_actual: int = 0
    iteracion_maxima: int = 0
    valor_inicial: float = 0
    valor_anterior: float = 0

    def __init__(
        self,
        funcion: Funcion2d,
        derivada_funcion: Funcion2d,
        iteraciones: int,
        valor_inicial: float,
    ):
        if not iteraciones >= 1:
            raise Exception("El numero de iteraciones deben ser mayores a 0")

        self.funcion = funcion
        self.derivada_funcion = derivada_funcion
        self.iteracion_maxima = iteraciones
        self.valor_inicial = valor_inicial

    def __iter__(self):
        return self

    def get_criterio(self, x_i: float, f_x: float, f_derivada_x: float) -> float:
        return x_i - f_x / f_derivada_x

    def __next__(self) -> IteracionNewton:
        if self.iteracion_actual == self.iteracion_maxima:
            raise StopIteration
        self.iteracion_actual += 1
        x_i: float = (
            self.valor_inicial if self.iteracion_actual == 1 else self.valor_anterior
        )
        f_x: float = self.funcion(x_i)
        f_derivada_x: float = self.derivada_funcion(x_i)
        criterio: float = self.get_criterio(x_i, f_x, f_derivada_x)
        if self.iteracion_actual != 1:
            self.error_relativo = get_error_relativo(self.valor_anterior, criterio)
        self.valor_anterior = criterio
        self.filaActual = IteracionNewton(
            x_i=x_i,
            f_x=f_x,
            f_derivada_x=f_derivada_x,
            error_relativo=self.error_relativo,
            criterio=criterio,
            iteracion=self.iteracion_actual,
        )
        self.calculado = True
        return self.filaActual


if __name__ == "__main__":

    def funcion(valor: float) -> float:
        return exp(-1 * valor) - valor

    def derivada_funcion(valor: float) -> float:
        return -1 * exp(-1 * valor) - 1

    iteraciones: int = 15
    for fila in Newton(funcion, derivada_funcion, 3, 0):
        print(fila, "\n")
