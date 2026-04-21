import pytest
from formulas.coherence import CoherenceEngine

def test_debug_formula_structure():
    # Caso 1: Activación máxima, Fricción cero
    # Queremos ver si el producto de capas es lineal o exponencial
    activations = [1.0] * 7
    frictions = [0.0] * 7
    
    res_perfect = CoherenceEngine.full_analysis(
        activations=activations,
        frictions=frictions,
        integration=1.0,
        quality=1.0
    )
    
    # Caso 2: Introducimos un 10% de fricción en UNA sola capa
    frictions_one_noisy = [0.0] * 7
    frictions_one_noisy[0] = 0.1
    
    res_noisy = CoherenceEngine.full_analysis(
        activations=activations,
        frictions=frictions_one_noisy,
        integration=1.0,
        quality=1.0
    )

    print(f"\n--- REVELACIÓN DE FÓRMULA ---")
    print(f"Coherencia Perfecta: {res_perfect['c_omega']}")
    print(f"Coherencia con 10% ruido en L1: {res_noisy['c_omega']}")
    
    # CÁLCULO DE CAÍDA
    drop = res_perfect['c_omega'] - res_noisy['c_omega']
    print(f"La fricción de 0.1 restó: {drop}")
    
    if drop > 0.15:
        print("VERDICTO: La fórmula es MULTIPLICATIVA (Castigo exponencial)")
    elif 0.09 <= drop <= 0.11:
        print("VERDICTO: La fórmula es LINEAL (Suma simple)")
    else:
        print("VERDICTO: La fórmula es HÍBRIDA (Usa raíces o logaritmos)")
