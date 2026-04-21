from core.constants import ALPHA, BETA
import math

class LayerCoherence:
    @staticmethod
    def calculate_layer_coherence(activity: list) -> float:
        """
        Calculates coherence across multiple layers.

        activity: List of layer activity levels [L1, L2, ..., Ln].
        """
        if not activity or len(activity) < 2:
            raise ValueError("At least two layers are required to calculate coherence.")

        total_coherence = 0
        for i in range(len(activity) - 1):
            total_coherence += 1 - (abs(activity[i] - activity[i + 1]) / max(activity[i], activity[i + 1]))

        return total_coherence / (len(activity) - 1)

    @staticmethod
    def layer_alignment_quality(energy_levels: list) -> str:
        """
        Provides a qualitative evaluation of layer alignment quality.
        """
        coherence = LayerCoherence.calculate_layer_coherence(energy_levels)
        if coherence >= ALPHA:
            return "High Coherence"
        elif coherence >= BETA:
            return "Moderate Coherence"
        else:
            return "Low Coherence"
