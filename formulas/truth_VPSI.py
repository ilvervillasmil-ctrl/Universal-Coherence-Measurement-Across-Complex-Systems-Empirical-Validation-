"""
formulas/truth_VPSI.py — Implementación Canónica del Structural Truth Theorem.
Basado en VPSI v9.2 de Ilver Villasmil (2026).

AXIOMÁTICA DEL SISTEMA (Pág. 32-35):
1. Axioma de Existencia (R): La realidad física R es absoluta e independiente.
2. Axioma de la Fracción β: El piso mínimo de verdad es 1/27.
3. Axioma de la Cota α: La descripción máxima posible es 26/27.
4. Axioma de Unidad: α + β = 1 (La suma de lo observable y lo oculto).
5. Axioma de Interdependencia: Tru(D) requiere la concurrencia de C, L y K.
6. Axioma de Cota Informacional: Ninguna Ri puede generar información mayor a R.
7. Axioma de Invariancia: La estructura del cubo es la base de toda verdad en R3.
"""

from formulas.constants import ALPHA, BETA

class TruthTheorem:
    """
    Motor de Verdad Estructural.
    Implementa la fórmula canónica: Trutotal = C · L · K · α + β
    """

    @staticmethod
    def compute_total_truth(c: float, l: float, k: float) -> float:
        """
        Calcula la Verdad Total (Trutotal) de una descripción D.
        
        Sintaxis exacta del documento (Pág. 11):
        Trutotal(D) = C * L * K * α + β
        
        Donde:
        - C (Coherencia): Sincronía interna del sistema.
        - L (Lógica): Validez del procesamiento formal.
        - K (Correlación): Evidencia causal de Ocontext.
        """
        # Asegurar límites físicos [0, 1] para los componentes
        c_val = max(0.0, min(1.0, c))
        l_val = max(0.0, min(1.0, l))
        k_val = max(0.0, min(1.0, k))
        
        # Tru_Ri: La verdad desde la perspectiva del observador (Subjetiva)
        tru_ri = c_val * l_val * k_val
        
        # Trutotal: La verdad anclada a la estructura física (Objetiva)
        # El resultado nunca puede ser 0.0 debido al Axioma 2 (+BETA).
        truth_total = (tru_ri * ALPHA) + BETA
        
        return truth_total

    @staticmethod
    def get_formal_definition():
        """Retorna la definición formal para diagnósticos del sistema."""
        return {
            "canonical_formula": "Trutotal(D) = C * L * K * α + β",
            "floor_value": BETA,
            "max_observable": ALPHA,
            "verification": "ALPHA + BETA == 1.0"
        }
