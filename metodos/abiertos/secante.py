from metodos.tipos import IteracionABC


class IteracionSecante(IteracionABC):
    error_relativo: float
    x_i_actual: float
    x_i_anterior: float
    x_i_siguiente: float
    iteracion: int

    def obtener_x_i(self) -> float:
        return self.x_i_siguiente

    def obtener_iteracion(self) -> int:
        return self.iteracion

    def obtener_error_relativo(self) -> float:
        return self.error_relativo
