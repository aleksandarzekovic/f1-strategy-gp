"""
Decision tree node for F1 strategy
"""

from typing import Optional
from ..models import RaceState, Decision, TyreCompound


class StrategyNode:
    """Node in decision tree - can be condition or action"""

    def __init__(
        self,
        node_type: str,
        condition: Optional[str] = None,
        left: Optional['StrategyNode'] = None,
        right: Optional['StrategyNode'] = None,
        decision_value: Optional[Decision] = None
    ):
        self.node_type = node_type  # 'condition' or 'action'
        self.condition = condition  # Condition to check
        self.left = left           # Left branch (if true)
        self.right = right         # Right branch (if false)
        self.decision_value = decision_value  # Action if leaf

    def evaluate(self, state: RaceState) -> Decision:
        """Evaluate decision tree based on race state"""
        if self.node_type == 'action':
            return self.decision_value

        # Evaluate condition
        condition_result = self._evaluate_condition(state)

        if condition_result and self.left:
            return self.left.evaluate(state)
        elif not condition_result and self.right:
            return self.right.evaluate(state)
        else:
            # Default action
            return Decision(
                pit_now=False,
                target_compound=TyreCompound.MEDIUM,
                aggressive_pace=False
            )

    def _evaluate_condition(self, state: RaceState) -> bool:
        """Check if condition is met"""
        try:
            # Create namespace with state
            namespace = {
                'current_lap': state.current_lap,
                'tyre_age': state.tyre_age,
                'position': state.position,
                'gap_to_leader': state.gap_to_leader,
                'gap_to_rival': state.gap_to_rival,
                'safety_car': state.safety_car,
                'rain_probability': state.rain_probability,
                'pit_stops_made': state.pit_stops_made,
                'track_wetness': state.track_wetness,
                'is_soft': state.tyre_compound == TyreCompound.SOFT,
                'is_medium': state.tyre_compound == TyreCompound.MEDIUM,
                'is_hard': state.tyre_compound == TyreCompound.HARD,
                'is_intermediate': state.tyre_compound == TyreCompound.INTERMEDIATE,
                'is_wet': state.tyre_compound == TyreCompound.WET,
                'on_dry_tyres': state.is_dry_tyres(),
                'on_wet_tyres': state.is_wet_tyres(),
            }
            return eval(self.condition, {"__builtins__": {}}, namespace)
        except Exception:
            return False

    def visualize(self, depth: int = 0, prefix: str = "") -> str:
        """Generate string visualization of tree"""
        indent = "  " * depth
        result = []

        if self.node_type == 'action':
            d = self.decision_value
            result.append(
                f"{indent}{prefix}→ PIT: {d.pit_now}, "
                f"TYRES: {d.target_compound.compound_name}, "
                f"PUSH: {d.aggressive_pace}"
            )
        else:
            result.append(f"{indent}{prefix}? {self.condition}")
            if self.left:
                result.append(self.left.visualize(depth + 1, "Y "))
            if self.right:
                result.append(self.right.visualize(depth + 1, "N "))

        return "\n".join(result)
