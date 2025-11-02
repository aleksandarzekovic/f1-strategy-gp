"""
F1 Strategy Program - evolves decision trees
"""

import random
from typing import List
from .decision_tree import StrategyNode
from ..models import Decision, TyreCompound, RaceState


class StrategyProgram:
    """Program that makes strategic F1 decisions"""

    # Pool of conditions to choose from
    CONDITIONS_POOL = [
        # Tyre age conditions
        'tyre_age > 25',
        'tyre_age > 20',
        'tyre_age > 15',
        'tyre_age > 10',
        'tyre_age < 5',

        # Lap conditions
        'current_lap > 35',
        'current_lap > 25',
        'current_lap > 15',
        'current_lap < 10',

        # Position conditions
        'position <= 3',
        'position <= 5',
        'position > 10',
        'position > 15',

        # Gap conditions
        'gap_to_rival < 1.0',
        'gap_to_rival < 2.0',
        'gap_to_rival > 5.0',
        'gap_to_leader < 10.0',

        # Event conditions
        'safety_car',
        'rain_probability > 0.5',
        'rain_probability > 0.7',
        'track_wetness > 0.3',
        'track_wetness > 0.6',

        # Pit stop conditions
        'pit_stops_made == 0',
        'pit_stops_made == 1',
        'pit_stops_made >= 2',

        # Tyre type conditions
        'is_soft and tyre_age > 12',
        'is_medium and tyre_age > 20',
        'is_hard and tyre_age > 25',
        'on_dry_tyres and track_wetness > 0.3',
        'on_wet_tyres and track_wetness < 0.2',
    ]

    def __init__(self, max_depth: int = 4):
        self.max_depth = max_depth
        self.decision_tree = self._create_random_tree(depth=0)
        self.fitness = float('inf')

    def _create_random_tree(self, depth: int) -> StrategyNode:
        """Create random decision tree"""

        # If max depth reached, create action (leaf)
        if depth >= self.max_depth:
            return self._create_random_action()

        # Otherwise create condition node
        condition = random.choice(self.CONDITIONS_POOL)

        return StrategyNode(
            node_type='condition',
            condition=condition,
            left=self._create_random_tree(depth + 1),
            right=self._create_random_tree(depth + 1)
        )

    def _create_random_action(self) -> StrategyNode:
        """Create random action node"""
        return StrategyNode(
            node_type='action',
            decision_value=Decision(
                pit_now=random.choice([True, False]),
                target_compound=random.choice(list(TyreCompound)),
                aggressive_pace=random.choice([True, False])
            )
        )

    def make_decision(self, state: RaceState) -> Decision:
        """Make decision based on race state"""
        return self.decision_tree.evaluate(state)

    def visualize(self) -> str:
        """Display decision tree"""
        return self.decision_tree.visualize()

    def __str__(self):
        return f"StrategyProgram(fitness={self.fitness:.2f})"
