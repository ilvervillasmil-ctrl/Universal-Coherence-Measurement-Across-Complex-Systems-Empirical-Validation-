import math
from formulas.coherence import CoherenceEngine
from formulas.constants import ALPHA, BETA, KAPPA, THETA_CUBE, R_FIN


def test_c_beta_all_active():
    """C_beta with all layers fully active produces a positive value."""
    activations = [1.0] * 7
    result = CoherenceEngine.compute_c_beta(activations)
    assert result["c_beta"] > 0


def test_c_beta_one_zero_collapses():
    """If any layer is zero, C_beta product collapses."""
    activations = [1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0]
    result = CoherenceEngine.compute_c_beta(activations)
    assert result["c_beta"] == 0.0


def test_c_beta_has_all_components():
    """C_beta result includes all expected keys."""
    activations = [0.8] * 7
    result = CoherenceEngine.compute_c_beta(activations)
    for key in ["c_beta", "energies", "product", "alpha_over_s", "r_fin", "rho", "p_t", "wonder", "i_ext"]:
        assert key in result


def test_c_alpha_basic():
    """C_alpha = I*Q / (D + U + beta)."""
    result = CoherenceEngine.compute_c_alpha(1.0, 1.0, 1.0, 0.0)
    expected = 1.0 / (1.0 + 0.0 + BETA)
    assert abs(result["c_alpha"] - expected) < 1e-10


def test_c_alpha_zero_integration():
    """Zero integration = zero C_alpha."""
    result = CoherenceEngine.compute_c_alpha(0.0, 1.0, 1.0, 0.0)
    assert result["c_alpha"] == 0.0


def test_c_total_pythagorean():
    """C_total = sqrt(C_beta^2 + C_alpha^2)."""
    result = CoherenceEngine.compute_c_total(3.0, 4.0)
    assert abs(result["c_total"] - 5.0) < 1e-10


def test_c_total_balance_centered():
    """When theta matches cube angle, balance is CENTERED."""
    c_beta = math.sin(THETA_CUBE)
    c_alpha = math.cos(THETA_CUBE)
    result = CoherenceEngine.compute_c_total(c_beta, c_alpha)
    assert result["balance"] == "CENTERED"


def test_c_total_zero_zero():
    """Both zero = total zero."""
    result = CoherenceEngine.compute_c_total(0.0, 0.0)
    assert result["c_total"] == 0.0


def test_basic_formula():
    """C = alpha * H + beta * I_ext."""
    energies = [1.0] * 7
    result = CoherenceEngine.compute_basic(energies, i_ext=1.0)
    assert abs(result["c_omega"] - (ALPHA * 0.0 + BETA * 1.0)) < 1e-10


def test_full_analysis_returns_all():
    """full_analysis returns all expected sections."""
    activations = [0.8] * 7
    result = CoherenceEngine.full_analysis(activations)
    for key in ["c_beta", "c_alpha", "c_total", "negentropy", "metaconsciousness", "mc_level", "resonance", "diagnostic_code", "diagnostic_name", "four_pillars"]:
        assert key in result


def test_full_analysis_four_pillars():
    """Four pillars are present with correct values."""
    activations = [0.8] * 7
    result = CoherenceEngine.full_analysis(activations)
    pillars = result["four_pillars"]
    assert pillars["beta"] == BETA
    assert pillars["kappa"] == KAPPA
    assert pillars["alpha"] == ALPHA


def test_metacube_recursion():
    """Metacube level returns correct structure."""
    result = CoherenceEngine.metacube_level(0.5, level=0)
    assert result["level"] == 0
    assert result["is_beta_of_level"] == 1
    assert result["ratio_alpha_beta"] == ALPHA / BETA
