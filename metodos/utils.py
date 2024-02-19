def get_error_relativo(r_actual: float, r_anterior: float) -> float:
    return abs((r_actual - r_anterior) / r_actual)
