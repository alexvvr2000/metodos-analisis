from dataclasses import dataclass
from math import exp
from typing import Callable

from metodos.tipos import Funcion2d, IteracionABC
from metodos.utils import get_error_relativo


@dataclass
class IteracionPosicionFalsa(IteracionABC):
    valor_a: float
    valor_b: float
    valor_r: float
    f_a: float
    f_r: float
    error_relativo: float
    criterio: float
    iteracion: int

    def obtener_error_relativo(self) -> float:
        return self.error_relativo

    def obtener_x_i(self) -> float:
        return self.valor_r

    def obtener_iteracion(self) -> int:
        return self.iteracion


class PosicionFalsa:
    funcion: Funcion2d
    filaActual: IteracionPosicionFalsa
    error_relativo: float = -1
    calculado: bool = False
    a_actual: float = 0
    b_actual: float = 0
    r_actual: float = 0
    iteracion_actual: int = 0
    iteracion_maxima: int = 0

    def __init__(self, funcion: Funcion2d, a: float, b: float, iteraciones: int):
        if a > b:
            raise Exception("El valor a tiene que ser menor a b")

        if not iteraciones >= 1:
            raise Exception("El numero de iteraciones deben ser mayores a 0")

        self.funcion = funcion
        self.a_actual = a
        self.b_actual = b
        self.iteracion_maxima = iteraciones

    def __iter__(self):
        return self

    def get_r(self, valor_a: float, valor_b: float) -> float:
        return valor_b - (self.funcion(valor_b) * (valor_a - valor_b)) / (
            self.funcion(valor_a) - self.funcion(valor_b)
        )

    def __next__(self) -> IteracionPosicionFalsa:
        if self.iteracion_actual == self.iteracion_maxima:
            raise StopIteration
        self.iteracion_actual += 1
        a_actual: float = self.a_actual
        b_actual: float = self.b_actual
        r_actual: float = self.get_r(a_actual, b_actual)
        error_actual: float = -1
        if self.calculado:
            r_anterior: float = self.filaActual.valor_r
            error_actual: float = get_error_relativo(r_actual, r_anterior)
        self.error_actual = error_actual
        f_a: float = self.funcion(a_actual)
        f_r: float = self.funcion(r_actual)
        criterio: float = f_a * f_r
        if f_r == 0:
            raise StopIteration
        elif criterio < 0:
            self.a_actual = a_actual
            self.b_actual = r_actual
        else:
            self.a_actual = r_actual
            self.b_actual = b_actual
        self.filaActual = IteracionPosicionFalsa(
            valor_a=a_actual,
            valor_b=b_actual,
            valor_r=r_actual,
            f_a=f_a,
            f_r=f_r,
            error_relativo=error_actual,
            criterio=criterio,
            iteracion=self.iteracion_actual,
        )
        self.calculado = True
        return self.filaActual


if __name__ == "__main__":

    def funcion(x: float) -> float:
        return exp(-x) - x

    for filaActual in PosicionFalsa(funcion, 0, 1, 3):
        print(filaActual, "\n")
