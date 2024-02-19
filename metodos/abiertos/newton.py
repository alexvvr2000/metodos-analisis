from dataclasses import dataclass
from math import exp
from os import path, remove
from typing import Callable, Tuple


@dataclass
class FilaMetodo:
    x_i: float
    f_x: float
    f_derivada_x: float
    criterio: float
    error_relativo: float


class Newton:
    funcion: Callable[[float], float]
    derivada_funcion: Callable[[float], float]
    filaActual: FilaMetodo
    error_relativo: float = -1
    calculado: bool = False
    x_anterior: float
    iteracion_actual: int = 0
    iteracion_maxima: int = 0
    valor_inicial: float = 0
    valor_anterior: float = 0

    def __init__(
        self,
        funcion: Callable[[float], float],
        derivada_funcion: Callable[[float], float],
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

    def get_error_relativo(self, valor_actual: float, valor_anterior: float) -> float:
        return abs((valor_anterior - valor_actual) / valor_anterior)

    def get_criterio(self, x_i: float, f_x: float, f_derivada_x: float) -> float:
        return x_i - f_x / f_derivada_x

    def __next__(self) -> Tuple[FilaMetodo, int]:
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
            self.error_relativo = self.get_error_relativo(self.valor_anterior, criterio)
        self.valor_anterior = criterio
        self.filaActual = FilaMetodo(
            x_i=x_i,
            f_x=f_x,
            f_derivada_x=f_derivada_x,
            error_relativo=self.error_relativo,
            criterio=criterio,
        )
        self.calculado = True
        return self.filaActual, self.iteracion_actual


if __name__ == "__main__":

    def funcion(valor: float) -> float:
        return exp(-1 * valor) - valor

    def derivada_funcion(valor: float) -> float:
        return -1 * exp(-1 * valor) - 1

    def nuevaLinea(linea: str, archivo: str) -> None:
        with open(archivo, "a") as csv:
            csv.write(linea)

    archivo = "prueba.csv"
    if path.exists(archivo):
        remove(archivo)
    iteraciones: int = 15
    nuevaLinea("iteracion,x_i,f(xi),f'(xi),x_i+1,error", archivo)
    for fila, iteracion in Newton(funcion, derivada_funcion, 3, 0):
        print(fila, "\n")
