"""
examples/compute_example.py

Script de ejemplo para calcular C usando la implementación estructural.
No modifica ninguna constante de marco; solo ilustra resultados bajo dos convenciones.
"""

from src.compute_coherence_structural import compute_C_from_S, C_MAX

def main():
    # Valores del README
    S_example = 1.285
    omega_U = 0.85
    R_fin = 0.75

    # Dos convenciones de escala
    S_ref_convenio = 1.222  # convención histórica usada en el estudio
    S_ref_teorico = 6.0     # convención teórica pura (N=6)

    c1 = compute_C_from_S(S_example, omega_U, R_fin, C_MAX, S_ref_convenio)
    c2 = compute_C_from_S(S_example, omega_U, R_fin, C_MAX, S_ref_teorico)

    print("Resultados de ejemplo:")
    print(f"  Convención estudio (S_ref={S_ref_convenio}): C = {c1:.3f}")
    print(f"  Convención teórica (S_ref={S_ref_teorico}): C = {c2:.3f}")

if __name__ == "__main__":
    main()
