import pytest
from core.engine import OmegaEngine
from formulas.constants import ALPHA, CODE_LOOP

def test_forced_architect_perfection():
    """
    Simulación de 'Perfección Estática'. 
    Busca alcanzar el CODE 9000 (Architect) y observar si 
    el sistema detecta el CODE 9999 (Loop) tras varias iteraciones.
    """
    engine = OmegaEngine()
    
    # 1. Inyectamos perfección absoluta que cumple con el Validador
    # L6 debe ser 0.0 para no disparar PurposeAlignmentError
    activations = [1.0] * 7
    frictions = [0.0] * 7 
    
    # 2. Corremos el motor varias veces con los mismos datos exactos
    # El sistema v3.2 detecta bucles tras 5 ciclos (LOOP_WINDOW) sin varianza
    results = []
    for _ in range(6):
        # El motor internamente llama al validador
        c_omega = engine.state.update(activations=activations, frictions=frictions)
        results.append(c_omega)
    
    final_state = engine.state
    
    # 3. Verificaciones de la 'Mentira Perfecta'
    # La coherencia debe ser exactamente ALPHA (0.9629...) por el clamp de seguridad
    assert results[-1] == ALPHA
    
    # 4. Prueba de Fuego: ¿Nos detectó el detector de bucles (Dynamics)?
    # Al no haber varianza (variance < LOOP_VARIANCE), debería activar el CODE_LOOP
    is_loop = final_state.detect_loop(final_state.history)
    
    print(f"\n[RESULTADO] C_Ω: {results[-1]}")
    print(f"[LOOP DETECTED]: {is_loop}")
    
    if is_loop:
        print("Misión cumplida: El sistema detectó que la perfección era un bucle estático.")
