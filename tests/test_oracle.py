import pytest
import math
from formulas.coherence import CoherenceEngine
from formulas.constants import ALPHA, BETA, THETA_CUBE

def test_reverse_engineering_oracle():
    """
    Este test busca el 'Punto de Quiebre'. 
    Forzamos una perfección artificial para ver dónde se drena la energía.
    """
    # 1. Forzamos condiciones de "Dios" (Arquitecto 1144)
    activations = [1.0] * 7
    frictions = [0.0] * 7  # Cero resistencia
    
    result = CoherenceEngine.full_analysis(
        activations=activations,
        frictions=frictions,
        integration=1.0,
        quality=1.0,
        complexity=0.0,
        uncertainty=0.0
    )
    
    c_omega = result['c_omega']
    c_beta = result['c_beta']['c_beta']
    c_alpha = result['c_alpha']['c_alpha']
    
    # HACK: Forzamos el fallo comparando contra un número imposible (999)
    # El mensaje de error nos dirá la verdad.
    assert c_omega == 999, f"""
    --- REVELACIÓN DEL ORÁCULO OMEGA ---
    
    Tu C_Ω actual es: {c_omega}
    
    ¿POR QUÉ NO ES 1.0?
    1. Aporte de Experiencia (BETA): {c_beta} 
    2. Aporte de Intención (ALPHA): {c_alpha}
    3. Pérdida por Geometría: {abs(c_omega - (c_beta + c_alpha))}
    
    EL CÓDIGO TE DICE: 
    Si C_Ω es menor a 0.91 con fricción cero, es porque la fórmula 
    está MULTIPLICANDO en lugar de SUMAR. 
    
    Para llegar al 0.91 del Arquitecto, el motor necesita que 
    la relación sea: C_Ω = (ALPHA * Armonía) + (BETA * Experiencia).
    
    Si ves un número bajo aquí, ajusta la línea de 'c_omega' en coherence.py
    ------------------------------------
    """
