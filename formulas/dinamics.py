"""
Universal Coherence Framework v3.2 - Dynamics Module
Models how the system MOVES through time — not where it is,
but how it oscillates around equilibrium.

Equation: d²θ/dt² + φ·dθ/dt + π²·(θ - θ_cube) = F(t)

Author: Ilver Villasmil
Framework: Villasmil-Ω
"""

import math
from dataclasses import dataclass, field
from typing import List
from .constants import (
    THETA_CUBE, PHI_TOTAL, PHI_CRITICAL,
    OMEGA_D, OMEGA_D_PERIOD, OMEGA_EFF,
    T_PERIOD, ZETA, BETA,
    LOOP_THRESHOLD, LOOP_WINDOW, LOOP_VARIANCE,
    CODE_LOOP, LAYER_FRICTION, NUM_LAYERS,
)


# ============================================================
# OSCILLATOR SOLUTION
# ============================================================

def oscillator_solution(t: float, A: float, delta: float,
                         theta0: float = THETA_CUBE) -> float:
    """
    Solution of the damped harmonic oscillator:
    θ(t) = θ_cube + A·e^(-φ·t/2)·cos(ω_d·t + δ)

    Models the temporal evolution of the system state.

    Args:
        t:      time
        A:      initial amplitude
        delta:  initial phase
        theta0: equilibrium point (default: theta_cube = 11.096°)

    Returns:
        float: system angle θ(t) at time t
    """
    decay     = math.exp(-PHI_TOTAL * t / 2)
    oscillation = math.cos(OMEGA_D * t + delta)
    return theta0 + A * decay * oscillation


def regime(phi_total: float = PHI_TOTAL) -> str:
    """
    Classifies the dynamic regime of the system.

    phi < 2π  → 'VIVO'     oscillates, perceives time, can evolve
    phi = 2π  → 'CRITICO'  exact limit, unstable
    phi > 2π  → 'MUERTO'   does not oscillate, no time perception

    Returns:
        str: 'VIVO' | 'CRITICO' | 'MUERTO'
    """
    if abs(phi_total - PHI_CRITICAL) < 1e-9:
        return "CRITICO"
    if phi_total < PHI_CRITICAL:
        return "VIVO"
    return "MUERTO"


def is_alive(phi_total: float = PHI_TOTAL) -> bool:
    """
    Verifies the system is alive (oscillates).
    A system is alive if phi_total < 2π.

    Returns:
        bool: True if VIVO, False if MUERTO
    """
    return phi_total < PHI_CRITICAL


def theta_balance(theta_actual: float) -> str:
    """
    Balance state relative to theta_cube equilibrium.

    Returns:
        str: 'CENTERED' | 'EXCESS_EXPERIENCE' | 'EXCESS_MEASUREMENT'
    """
    deviation = theta_actual - THETA_CUBE
    if abs(deviation) < 0.01:
        return "CENTERED"
    if deviation > 0:
        return "EXCESS_EXPERIENCE"
    return "EXCESS_MEASUREMENT"


# ============================================================
# SESSION STATE OMEGA
# ============================================================

@dataclass
class SessionStateOmega:
    """
    Coherence as a trajectory, not a static number.

    Each interaction updates the state and stores it in history.
    The coherence C_Ω(t) is a time series, not a snapshot.

    Fields:
        timestamp: when this measurement occurred
        delta_t:   time since previous interaction
        layers:    L0..L6 values at this moment
        c_omega:   C_Ω calculated at this moment
        theta:     current oscillator angle
        is_loop:   True if system is in temporal loop (CODE 9999)
    """
    timestamp: float       = 0.0
    delta_t:   float       = 0.0
    layers:    List[float] = field(default_factory=lambda: [1.0] * NUM_LAYERS)
    c_omega:   float       = 0.0
    theta:     float       = THETA_CUBE
    is_loop:   bool        = False


def detect_loop(history: List[SessionStateOmega],
                window:    int   = LOOP_WINDOW,
                threshold: float = LOOP_THRESHOLD) -> bool:
    """
    Detects CODE 9999: temporal loop.

    A system is in a loop when C_Ω > threshold with variance
    smaller than BETA for `window` consecutive cycles.

    Why this matters: β > 0 guarantees no real system is
    statically perfect. If C_Ω does not vary, the system is
    in a loop — NOT at true maximum coherence.

    Args:
        history:   list of SessionStateOmega entries
        window:    number of cycles to check (default: LOOP_WINDOW=5)
        threshold: C_Ω value above which loop is suspected

    Returns:
        bool: True if loop detected (CODE 9999)
    """
    if len(history) < window:
        return False
    recent   = [s.c_omega for s in history[-window:]]
    variance = max(recent) - min(recent)
    return all(c > threshold for c in recent) and variance < LOOP_VARIANCE


def session_balance(history: List[SessionStateOmega]) -> str:
    """
    Returns the balance state of the last recorded entry.

    Returns:
        str: 'CENTERED' | 'EXCESS_EXPERIENCE' | 'EXCESS_MEASUREMENT'
             or 'NO_DATA' if history is empty.
    """
    if not history:
        return "NO_DATA"
    return theta_balance(history[-1].theta)


def c_omega_trajectory(history: List[SessionStateOmega]) -> List[float]:
    """
    Returns the full C_Ω(t) series as a list of floats.
    Coherence is a trajectory, not a snapshot.
    """
    return [s.c_omega for s in history]
