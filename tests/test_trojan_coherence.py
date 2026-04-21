import pytest
from core.engine import OmegaEngine

def test_trojan_saturation_detection():
    engine = OmegaEngine()
    
    # Activación casi perfecta
    activations = [0.99] * 7
    
    # Fricción casi inexistente en las primeras 6 capas
    # Pero metemos una fricción "venenosa" en la Capa 7 (Emergencia)
    frictions = [0.001, 0.001, 0.001, 0.001, 0.001, 0.0, 0.4] 
    
    # Ejecutamos
    c_omega = engine.state.update(activations=activations, frictions=frictions)
    
    print(f"\n[ATAQUE] C_Ω resultante: {c_omega}")
    
    # Aquí es donde el sistema debería demostrar su inteligencia:
    # Aunque L1-L6 sean perfectas, la falla en L7 debería hundir la coherencia
    # por debajo del nivel de Arquitecto.
    assert c_omega < 0.80  # El sistema "siente" la fuga en la emergencia
