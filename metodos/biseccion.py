from dataclasses import dataclass
from math import exp
from os import path, remove
from typing import Callable


@dataclass
class FilaMetodo:
    valor_a: float
    valor_b: float
    valor_r: float
    f_b: float
    f_r: float
    error_relativo: float
    criterio: float


class Biseccion:
    funcion: Callable[[float], float]
    filaActual: FilaMetodo
    error_relativo: float = -1
    calculado: bool = False
    a_actual: float = 0
    b_actual: float = 0
    r_actual: float = 0
    iteracion_actual: int = 0
    iteracion_maxima: int = 0

    def __init__(
        self, funcion: Callable[[float], float], a: float, b: float, iteraciones: int
    ):
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

    def get_error_relativo(self, r_actual: float, r_anterior: float) -> float:
        return abs((r_actual - r_anterior) / r_actual)

    def get_r(self, valor_a: float, valor_b: float) -> float:
        return (valor_a + valor_b) / 2

    def __next__(self) -> FilaMetodo, float:
        if self.iteracion_actual == self.iteracion_maxima:
            raise StopIteration
        self.iteracion_actual += 1
        a_actual: float = self.a_actual
        b_actual: float = self.b_actual
        r_actual: float = self.get_r(a_actual, b_actual)
        error_actual: float = -1
        if self.calculado:
            r_anterior: float = self.filaActual.valor_r
            error_actual: float = self.get_error_relativo(r_actual, r_anterior)
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
        self.filaActual = FilaMetodo(
            valor_a=a_actual,
            valor_b=b_actual,
            valor_r=r_actual,
            f_b=f_b,
            f_r=f_r,
            error_relativo=error_actual,
            criterio=criterio,
        )
        self.calculado = True
        return self.filaActual, self.iteracion_actual


def funcion(valor: float) -> float:
    return exp(-1 * valor) - valor


def nuevaLinea(linea: str, archivo: str) -> None:
    with open(archivo, "a") as csv:
        csv.write(linea)


if __name__ == "__main__":
    archivo = "prueba.csv"
    if path.exists(archivo):
        remove(archivo)
    iteraciones: int = 15
    nuevaLinea(
        "iteracion,valor_a,valor_b,valor_r,f_b,f_r,error_relativo,criterio\n", archivo
    )
    for fila, iteracion in Biseccion(funcion, 0, 1, iteraciones):
        valor_a: float = fila.valor_a
        valor_b: float = fila.valor_b
        valor_r: float = fila.valor_r
        f_b: float = fila.f_b
        f_r: float = fila.f_r
        error_relativo: float = fila.error_relativo
        criterio: float = fila.criterio
        nueva_linea: str = f"{iteracion},{valor_a},{valor_b},{valor_r},{f_b},{f_r},{error_relativo},{criterio}"
        if iteracion == iteraciones:
            nuevaLinea(nueva_linea, archivo)
        else:
            nuevaLinea(f"{nueva_linea}\n", archivo)
