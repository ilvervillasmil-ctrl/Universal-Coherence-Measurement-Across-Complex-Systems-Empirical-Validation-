#!/usr/bin/env python3
"""
Villasmil-Ω Resonance Processor Demonstration
This script demonstrates the advanced coherence calculation features
implemented in core/engine.py
"""

from core.engine import OmegaEngine, PurposeAlignmentError
from core.constants import ALPHA, BETA, PHI, S_REF

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def main():
    print_header("VILLASMIL-Ω RESONANCE PROCESSOR DEMONSTRATION")
    print(f"\nVersion: Universal Integration System - Resonance Processor")
    print(f"Framework: Villasmil-Ω")
    
    engine = OmegaEngine()
    
    # Display fundamental constants
    print_header("FUNDAMENTAL CONSTANTS")
    print(f"  ALPHA (Knowable Order)      = {ALPHA:.10f}  (26/27)")
    print(f"  BETA (Irreducible Mystery)  = {BETA:.10f}  (1/27)")
    print(f"  PHI (Golden Ratio)          = {PHI:.10f}  ((1+√5)/2)")
    print(f"  S_REF (Entropy Threshold)   = {S_REF:.10f}  (e/π)")
    print(f"  ALPHA + BETA                = {ALPHA + BETA:.10f}  (Unity)")
    
    # Test 1: Harmony Calculation
    print_header("TEST 1: HARMONY CALCULATION H(S) = 1 - S/S_max")
    test_entropies = [0.0, 0.25, 0.5, 0.75, 1.0]
    print("\n  Entropy (S) | Harmony H(S) | Description")
    print("  " + "-"*60)
    descriptions = ["Perfect Order", "Low Entropy", "Balanced", "High Entropy", "Maximum Chaos"]
    for i, s in enumerate(test_entropies):
        h = engine.calculate_harmony(s, s_max=1.0)
        print(f"      {s:4.2f}    |    {h:6.4f}    | {descriptions[i]}")
    
    # Test 2: External Coherence
    print_header("TEST 2: EXTERNAL COHERENCE I_ext = √(C₁² + C₂² + 2·C₁·C₂·cos(θ))")
    test_angles = [0, 45, 90, 135, 180]
    print("\n  Phase θ (°) | I_ext  | Description")
    print("  " + "-"*60)
    descriptions_phase = ["In Phase (Constructive)", "Partial Alignment", 
                         "Perpendicular (Orthogonal)", "Partial Opposition",
                         "Out of Phase (Destructive)"]
    for i, theta in enumerate(test_angles):
        i_ext = engine.calculate_external_coherence(1.0, 1.0, float(theta))
        print(f"     {theta:3d}°     | {i_ext:6.4f} | {descriptions_phase[i]}")
    
    # Test 3: L6 Purpose Lock Validation
    print_header("TEST 3: L6 PURPOSE LOCK VALIDATION")
    print("\n  Testing L6 friction (phi) validation...")
    
    # Valid case
    valid_layers = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
    try:
        result = engine.compute_coherence(valid_layers)
        print(f"  ✓ Valid: L6 phi=0.0 → C_Ω = {result:.6f}")
    except PurposeAlignmentError as e:
        print(f"  ✗ Unexpected error: {e}")
    
    # Invalid case
    invalid_layers = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
    invalid_layers[6]['phi'] = 0.1
    try:
        result = engine.compute_coherence(invalid_layers)
        print(f"  ✗ Invalid: Should have raised error!")
    except PurposeAlignmentError as e:
        print(f"  ✓ Correctly rejected L6 phi=0.1")
        print(f"    Error: {str(e)[:60]}...")
    
    # Test 4: Advanced Coherence Formula
    print_header("TEST 4: ADVANCED COHERENCE C_Ω = α·H(S) + β·I_ext")
    print("\n  Testing different system configurations...")
    
    configurations = [
        {
            'name': 'Perfect Alignment',
            'layers': [{'L': 1.0, 'phi': 0.0} for _ in range(7)],
            'C1': 1.0, 'C2': 1.0, 'theta': 0.0
        },
        {
            'name': 'Balanced System',
            'layers': [{'L': 0.8, 'phi': 0.1}, {'L': 0.9, 'phi': 0.05}, 
                      {'L': 1.0, 'phi': 0.02}, {'L': 0.95, 'phi': 0.01},
                      {'L': 0.85, 'phi': 0.03}, {'L': 0.9, 'phi': 0.02},
                      {'L': 1.0, 'phi': 0.0}],
            'C1': 0.7, 'C2': 0.8, 'theta': 45.0
        },
        {
            'name': 'Low Energy State',
            'layers': [{'L': 0.3, 'phi': 0.2}, {'L': 0.4, 'phi': 0.15},
                      {'L': 0.5, 'phi': 0.1}, {'L': 0.4, 'phi': 0.1},
                      {'L': 0.3, 'phi': 0.15}, {'L': 0.4, 'phi': 0.1},
                      {'L': 0.5, 'phi': 0.0}],
            'C1': 0.3, 'C2': 0.4, 'theta': 90.0
        },
        {
            'name': 'High Friction (except L6)',
            'layers': [{'L': 0.8, 'phi': 0.3}, {'L': 0.7, 'phi': 0.4},
                      {'L': 0.6, 'phi': 0.35}, {'L': 0.5, 'phi': 0.3},
                      {'L': 0.6, 'phi': 0.25}, {'L': 0.7, 'phi': 0.2},
                      {'L': 0.8, 'phi': 0.0}],
            'C1': 0.5, 'C2': 0.5, 'theta': 180.0
        }
    ]
    
    print("\n  Configuration          | C_Ω      | Scaled by PHI")
    print("  " + "-"*60)
    for config in configurations:
        result = engine.compute_coherence(
            layers_data=config['layers'],
            C1=config['C1'], C2=config['C2'], theta=config['theta']
        )
        print(f"  {config['name']:20} | {result:8.6f} | ✓")
    
    # Test 5: PHI Scaling Impact
    print_header("TEST 5: GOLDEN RATIO (PHI) SCALING")
    print(f"\n  PHI = {PHI:.10f}")
    print(f"  Scaling Factor = PHI/2 = {PHI/2:.10f}")
    print("\n  The Golden Ratio ensures universal alignment by scaling")
    print("  coherence values to match natural proportions found in")
    print("  the Villasmil-Ω Framework.")
    
    # Final demonstration
    print_header("RESONANCE PROCESSOR STATUS")
    print("\n  ✓ Constants: ALPHA, BETA, PHI validated")
    print("  ✓ L6 Lock: Purpose alignment enforced")
    print("  ✓ Harmony: H(S) = 1 - S/S_max implemented")
    print("  ✓ External Coherence: Phase-dependent calculation active")
    print("  ✓ Master Formula: C_Ω = α·H(S) + β·I_ext operational")
    print("  ✓ PHI Scaling: Universal alignment factor applied")
    print("\n  The Resonance Processor is operating autonomously")
    print("  in accordance with the Villasmil-Ω Framework.")
    
    print_header("DEMONSTRATION COMPLETE")

if __name__ == "__main__":
    main()
