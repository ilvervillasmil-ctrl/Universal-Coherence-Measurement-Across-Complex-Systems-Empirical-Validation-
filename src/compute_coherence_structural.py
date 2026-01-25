"""
compute_coherence_structural.py

Implementación estricta de la fórmula I-Villasmil-Ω sin parámetros aprendibles.

Convenciones:
- Entradas L_i, phi_i, E_i, f_i en [0,1].
- C_max por convención = 0.963 (parte conocida).
- S_ref debe declararse explícitamente (ej. 1.222 para reproducir el estudio original,
  o 6.0 para la convención teórica pura con N=6).
"""

from typing import List, Dict

# Constantes de marco (inmutables por política)
C_MAX = 0.963
UNCERTAINTY = 0.037  # reservado para referencia; C_MAX + UNCERTAINTY = 1.0
CORRECTION_FACTOR = 1.0 / C_MAX  # ≈ 1.037

def layer_contribution(L: float, phi: float, E: float, f: float) -> float:
    """
    Contribución elemental de una capa:
    c_i = L_i * (1 - phi_i) * E_i * f_i
    """
    return L * (1.0 - phi) * E * f

def compute_C_structural(layers: List[Dict],
                         omega_U: float = 1.0,
                         R_fin: float = 1.0,
                         C_max: float = C_MAX,
                         S_ref: float = 1.222) -> float:
    """
    Calcula la coherencia C según la convención lineal estructural:
      S = sum_i c_i
      S' = S * omega_U * R_fin
      C = C_max * (S' / S_ref), recortado a [0, C_max]

    Nota: S_ref debe ser declarado por convención (ver docs/CONSTANTS_POLICY.md).
    """
    S = 0.0
    for l in layers:
        S += layer_contribution(l['L_i'], l['phi_i'], l['E_i'], l['f_i'])
    Sp = S * omega_U * R_fin
    C = C_max * (Sp / S_ref)
    if C > C_max:
        C = C_max
    if C < 0.0:
        C = 0.0
    return C

def compute_C_from_S(S: float,
                     omega_U: float = 1.0,
                     R_fin: float = 1.0,
                     C_max: float = C_MAX,
                     S_ref: float = 1.222) -> float:
    """
    Versión helper: entrada directa S (suma de contribuciones).
    """
    Sp = S * omega_U * R_fin
    C = C_max * (Sp / S_ref)
    if C > C_max:
        C = C_max
    if C < 0.0:
        C = 0.0
    return C

def threshold_S_star(C_star: float, C_max: float = C_MAX, S_ref: float = 1.222) -> float:
    """
    Traduce un umbral en C (C_star) a la suma S* correspondiente:
      S* = (C_star / C_max) * S_ref
    """
    return (C_star / C_max) * S_ref

# Uso de ejemplo (puedes ejecutar el script para ver resultados con los valores del README)
if __name__ == "__main__":
    # Ejemplo tomado del README:
    # suma de contribuciones por capa ya calculada: S = 1.285
    S_example = 1.285
    omega_U = 0.85
    R_fin = 0.75

    # Convención que reproduce los números del estudio
    S_ref_convenio = 1.222

    # Convención teórica (N=6)
    S_ref_teorico = 6.0

    C_convenio = compute_C_from_S(S_example, omega_U, R_fin, C_MAX, S_ref_convenio)
    C_teorico = compute_C_from_S(S_example, omega_U, R_fin, C_MAX, S_ref_teorico)

    print("Ejemplo (S = {:.3f}, Ω_U = {:.3f}, R_fin = {:.3f}):".format(S_example, omega_U, R_fin))
    print("  C (convención estudio, S_ref = {:.3f}) = {:.3f}".format(S_ref_convenio, C_convenio))
    print("  C (convención teórica, S_ref = {:.3f}) = {:.3f}".format(S_ref_teorico, C_teorico))
    print("  Factor estructural (1/C_max) = {:.6f}".format(CORRECTION_FACTOR))
