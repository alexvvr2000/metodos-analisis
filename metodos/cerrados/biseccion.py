from dataclasses import dataclass
from math import exp

from metodos.tipos import Funcion2d, IteracionABC
from metodos.utils import get_error_relativo


@dataclass
class IteracionBiseccion(IteracionABC):
    valor_a: float
    valor_b: float
    valor_r: float
    f_b: float
    f_r: float
    error_relativo: float
    criterio: float
    iteracion: int

    def obtener_error_relativo(self) -> float:
        return self.error_relativo

    def obtener_iteracion(self) -> int:
        return self.iteracion

    def obtener_x_i(self) -> float:
        return self.valor_r


class Biseccion:
    funcion: Funcion2d
    filaActual: IteracionBiseccion
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
        return (valor_a + valor_b) / 2

    def __next__(self) -> IteracionBiseccion:
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
        f_b: float = self.funcion(b_actual)
        f_r: float = self.funcion(r_actual)
        criterio: float = f_b * f_r
        if criterio < 0:
            self.a_actual = r_actual
            self.b_actual = b_actual
        else:
            self.a_actual = a_actual
            self.b_actual = r_actual
        self.filaActual = IteracionBiseccion(
            iteracion=self.iteracion_actual,
            valor_a=a_actual,
            valor_b=b_actual,
            valor_r=r_actual,
            f_b=f_b,
            f_r=f_r,
            error_relativo=error_actual,
            criterio=criterio,
        )
        self.calculado = True
        return self.filaActual


if __name__ == "__main__":

    def funcion(valor: float) -> float:
        return exp(-1 * valor) - valor

    iteraciones: int = 15
    for fila in Biseccion(funcion, 0, 1, iteraciones):
        print(fila, "\n")
