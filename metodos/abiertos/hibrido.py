from dataclasses import dataclass

from metodos.abiertos.newton import Newton
from metodos.cerrados.biseccion import Biseccion
from metodos.tipos import Funcion2d, IteracionABC
from metodos.utils import get_error_relativo


@dataclass
class IteracionHibrido(IteracionABC):
    iteracion: int
    a_actual: float
    b_actual: float
    xi_actual: float
    xi_siguiente: float
    error_relativo: float

    def obtener_x_i(self) -> float:
        return self.xi_siguiente

    def obtener_iteracion(self) -> int:
        return self.iteracion

    def obtener_error_relativo(self) -> float:
        return self.error_relativo


class Hibrido:
    funcion: Funcion2d
    derivada: Funcion2d
    fila_anterior: IteracionHibrido
    xi_actual: float
    iteracion_maxima: int
    iteracion_actual: int = 0

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
        self.a_actual = a_inicial
        self.b_actual = b_inicial
        self.xi_actual = a_inicial

    def __iter__(self):
        return self

    def __next__(self) -> IteracionHibrido:
        if self.iteracion_actual >= self.iteracion_maxima:
            raise StopIteration

        if self.funcion(self.xi_actual) == 0:
            raise StopIteration

        a_actual: float = self.a_actual
        b_actual: float = self.b_actual
        xi_actual: float = self.xi_actual

        f_x: float = self.funcion(xi_actual)
        f_x_derivada: float = self.derivada(xi_actual)

        xi_siguiente: float = Newton.get_criterio(xi_actual, f_x, f_x_derivada)

        if not (a_actual <= xi_siguiente <= b_actual):
            xi_siguiente = Biseccion.get_r(a_actual, b_actual)

        if xi_siguiente < xi_actual:
            self.a_actual = xi_siguiente
        else:
            self.b_actual = xi_siguiente

        error_relativo: float = get_error_relativo(xi_siguiente, xi_actual)

        iteracion_actual = self.iteracion_actual
        self.iteracion_actual += 1

        self.fila_anterior = IteracionHibrido(
            iteracion=iteracion_actual,
            a_actual=a_actual,
            b_actual=b_actual,
            xi_siguiente=xi_siguiente,
            xi_actual=xi_actual,
            error_relativo=error_relativo,
        )

        self.xi_actual = xi_siguiente

        return self.fila_anterior


if __name__ == "__main__":

    def funcion(x: float) -> float:
        return x**2 - 2

    def derivada(x: float) -> float:
        return 2 * x

    for fila in Hibrido(funcion, derivada, 1, 2, 12):
        print(fila, "\n")
