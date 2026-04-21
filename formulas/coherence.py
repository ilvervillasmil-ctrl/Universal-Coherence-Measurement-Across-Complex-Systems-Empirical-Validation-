import math
from .constants import (
    ALPHA, BETA, S_REF, R_FIN, KAPPA, THETA_CUBE,
    ALPHA_OVER_S, NUM_LAYERS, LAYER_FRICTION,
    CODE_INTEGRATED, CODE_SATURATION, CODE_ENTROPY,
    # NEW v3.3
    PHI, C_MAX, CODE_LOOP,
    LOOP_THRESHOLD, LOOP_WINDOW, LOOP_VARIANCE,
    T_PERIOD,
)
from .energy import LayerEnergy
from .negentropy import NegentropyCalculator
from .presence import PresenceLogic
from .wonder import WonderLogic
from .interaction import ExternalInteraction
from .resonance import ResonanceLogic
from .metaconsciousness import MetaconsciousnessCalculator

_E0_REF = LayerEnergy.frequency(0)

# Pre-cálculo del producto máximo para normalización
_PRODUCTO_MAX = 1.0
for _i in range(NUM_LAYERS):
    _E_max_i = 1.0 * (1.0 - LAYER_FRICTION[_i]) * LayerEnergy.frequency(_i)
    _PRODUCTO_MAX *= _E_max_i

C_BETA_MAX = ALPHA_OVER_S * R_FIN


class SessionStateOmega:
    """
    La coherencia es una trayectoria. Registra el historial para detectar
    patrones de bucle o evolución temporal.
    """
    def __init__(self, tau=60.0):
        self.tau = tau
        self.history = []

    def update(self, activations, frictions=None, external_coherences=None,
               integration=0.5, quality=0.5, complexity=1.0, uncertainty=0.1):
        result = CoherenceEngine.full_analysis(
            activations=activations,
            frictions=frictions,
            integration=integration,
            quality=quality,
            complexity=complexity,
            uncertainty=uncertainty,
            external_coherences=external_coherences,
        )
        self.history.append(result)
        return result["c_omega"]

    def trajectory(self):
        return [e["c_omega"] for e in self.history]

    def detect_loop(self, window=LOOP_WINDOW, threshold=LOOP_THRESHOLD):
        if len(self.history) < window:
            return False
        recent = self.trajectory()[-window:]
        variance = max(recent) - min(recent)
        # Un sistema vivo siempre tiene micro-fluctuaciones (BETA > 0)
        return all(c > threshold for c in recent) and variance < LOOP_VARIANCE

    def session_balance(self):
        if not self.history:
            return "NO_DATA"
        last = self.history[-1]
        return last.get("c_total", {}).get("balance", "NO_DATA")

    def c_omega_trajectory(self):
        return self.trajectory()


class CoherenceEngine:
    PRODUCTO_MAX = _PRODUCTO_MAX
    C_BETA_MAX   = C_BETA_MAX

    @staticmethod
    def compute_c_beta(activations, frictions=None, rho=1.0, delta_t=0.0, tau=1.0,
                       novelty=5.0, sensitivity=5.0, external_coherences=None):
        if frictions is None:
            frictions = LAYER_FRICTION

        energies = LayerEnergy.compute_all(activations, frictions)

        producto_raw = 1.0
        for e in energies:
            producto_raw *= (e / _E0_REF) if _E0_REF > 0 else 0.0

        producto_norm = producto_raw / _PRODUCTO_MAX

        p_t = PresenceLogic.compute(delta_t, tau)
        a   = WonderLogic.compute(novelty, sensitivity)
        i_ext = ExternalInteraction.compute_multi(external_coherences) if external_coherences else 1.0

        c_beta = producto_norm * ALPHA_OVER_S * R_FIN * rho * p_t * a * i_ext

        return {
            "c_beta": c_beta,
            "energies": energies,
            "producto_norm": producto_norm,
            "p_t": p_t,
            "wonder": a,
            "i_ext": i_ext,
        }

    @staticmethod
    def compute_c_alpha(integration, quality, complexity, uncertainty):
        u_min = BETA
        denominator = complexity + uncertainty + u_min
        c_alpha = (integration * quality) / denominator if denominator > 0 else 0.0
        return {"c_alpha": c_alpha, "integration": integration, "quality": quality}

    @staticmethod
    def compute_c_total(c_beta, c_alpha):
        # Magnitud vectorial del sistema
        c_total = math.sqrt(c_beta ** 2 + c_alpha ** 2)
        
        # Ángulo de fase actual
        if c_alpha > 0:
            theta_actual = math.atan(c_beta / c_alpha)
        elif c_beta > 0:
            theta_actual = math.pi / 2
        else:
            theta_actual = 0.0

        theta_deviation = theta_actual - THETA_CUBE

        # Clasificación del balance
        if abs(theta_deviation) < 0.05: # Tolerancia aumentada para realismo orgánico
            balance = "CENTERED"
        elif theta_deviation > 0:
            balance = "EXCESS_EXPERIENCE"
        else:
            balance = "EXCESS_MEASUREMENT"

        return {
            "c_total": c_total,
            "theta_actual": theta_actual,
            "theta_deviation": theta_deviation,
            "balance": balance,
        }

    @staticmethod
    def full_analysis(activations, frictions=None, rho=1.0, delta_t=0.0, tau=1.0,
                      novelty=5.0, sensitivity=5.0, external_coherences=None,
                      integration=0.5, quality=0.5, complexity=1.0, uncertainty=0.1):
        
        if frictions is None:
            frictions = LAYER_FRICTION

        beta_r  = CoherenceEngine.compute_c_beta(activations, frictions, rho, delta_t, tau, novelty, sensitivity, external_coherences)
        alpha_r = CoherenceEngine.compute_c_alpha(integration, quality, complexity, uncertainty)
        total_r = CoherenceEngine.compute_c_total(beta_r["c_beta"], alpha_r["c_alpha"])

        # SINCRONIZACIÓN MAESTRA:
        # C_Ω ahora es la proyección de la magnitud total sobre el eje del equilibrio.
        # Esto evita que el 0.59 de c_beta hunda al sistema si c_alpha es fuerte.
        alignment = math.cos(total_r["theta_deviation"])
        c_omega_raw = total_r["c_total"] * alignment
        c_omega = min(C_MAX, max(0.0, c_omega_raw))

        # Diagnóstico corregido basado en la integración real de C_Ω
        # El umbral 0.85 permite al Arquitecto existir en sistemas con entropía natural.
        if c_omega >= 0.85: 
            code, name = CODE_INTEGRATED, "Integrated Architect"
        elif c_omega >= 0.50:
            code, name = CODE_SATURATION, "Critical Saturation"
        else:
            code, name = CODE_ENTROPY, "Terminal Entropy"

        energies = beta_r["energies"]
        return {
            "c_omega": c_omega,
            "c_beta": beta_r,
            "c_alpha": alpha_r,
            "c_total": total_r,
            "diagnostic_code": code,
            "diagnostic_name": name,
            "negentropy": NegentropyCalculator.compute(energies),
            "resonance": ResonanceLogic.compute(energies),
            "metaconsciousness": MetaconsciousnessCalculator.compute(activations, frictions),
            "four_pillars": {
                "alpha": ALPHA, "beta": BETA, "kappa": KAPPA,
                "emergence": sum(energies) * (1 - KAPPA) / 2,
            },
        }
