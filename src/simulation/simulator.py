"""
F1 Race simulator
"""

import random
from ..models import RaceState, TyreCompound
from ..strategy import StrategyProgram


class RaceSimulator:
    """Simulates F1 race and evaluates strategy"""

    def __init__(self, total_laps: int = 50):
        self.total_laps = total_laps
        self.pit_stop_time = 25.0  # Base pit stop time in seconds
        self.safety_car_pit_bonus = 10.0  # Time saved pitting under SC

    def simulate_race(self, strategy: StrategyProgram) -> float:
        """
        Simulate race and return score (lower = better)
        Returns total race time in seconds
        """
        state = self._initialize_race_state()
        total_time = 0.0

        for lap in range(self.total_laps):
            state.current_lap = lap

            # Random events
            self._process_random_events(state)

            # Make strategic decision
            decision = strategy.make_decision(state)

            # Apply pit stop decision
            if decision.pit_now:
                pit_time = self.pit_stop_time
                if state.safety_car:
                    pit_time -= self.safety_car_pit_bonus
                total_time += pit_time

                state.pit_stops_made += 1
                state.tyre_age = 0
                state.tyre_compound = decision.target_compound

            # Simulate lap
            lap_time = self._calculate_lap_time(state, decision.aggressive_pace)
            total_time += lap_time

            # Update state
            state.tyre_age += 1

        # Apply penalties
        total_time += self._calculate_penalties(state)

        return total_time

    def _initialize_race_state(self) -> RaceState:
        """Create initial race state"""
        return RaceState(
            current_lap=0,
            tyre_age=0,
            tyre_compound=TyreCompound.MEDIUM,
            position=random.randint(5, 15),
            gap_to_leader=random.uniform(5, 20),
            gap_to_rival=random.uniform(-3, 3),
            safety_car=False,
            rain_probability=0.1,
            pit_stops_made=0,
            track_wetness=0.0
        )

    def _process_random_events(self, state: RaceState):
        """Process random race events"""
        # Safety car
        if random.random() < 0.05:
            state.safety_car = True
        else:
            state.safety_car = False

        # Rain probability change
        if random.random() < 0.02:
            state.rain_probability = random.uniform(0.5, 0.9)

        # Track gets wet if raining
        if state.rain_probability > 0.5 and random.random() < 0.3:
            state.track_wetness = min(1.0, state.track_wetness + 0.2)
        else:
            state.track_wetness = max(0.0, state.track_wetness - 0.1)

    def _calculate_lap_time(self, state: RaceState, aggressive: bool) -> float:
        """Calculate lap time based on state"""
        base_time = 90.0  # Base lap time in seconds

        # Tyre degradation based on compound
        tyre_deg = self._calculate_tyre_degradation(state)

        # Base speed of different compounds (on dry track)
        compound_speed = self._calculate_compound_speed(state)

        lap_time = base_time + tyre_deg + compound_speed

        # Aggressive driving
        if aggressive:
            lap_time -= 0.3

        # Safety car
        if state.safety_car:
            lap_time += 10.0

        # Wrong tyres for conditions
        if state.track_wetness > 0.5 and state.is_dry_tyres():
            lap_time += 5.0  # Big penalty for dry tyres in wet
        elif state.track_wetness < 0.2 and state.is_wet_tyres():
            lap_time += 3.0  # Penalty for wet tyres on dry track

        return lap_time

    def _calculate_tyre_degradation(self, state: RaceState) -> float:
        """Calculate tyre degradation penalty"""
        degradation_rates = {
            TyreCompound.SOFT: 0.15,
            TyreCompound.MEDIUM: 0.08,
            TyreCompound.HARD: 0.05,
            TyreCompound.INTERMEDIATE: 0.10,
            TyreCompound.WET: 0.12,
        }
        return state.tyre_age * degradation_rates[state.tyre_compound]

    def _calculate_compound_speed(self, state: RaceState) -> float:
        """Calculate compound base speed modifier"""
        # Only applies on dry track
        if state.track_wetness > 0.3:
            return 0.0

        speed_modifiers = {
            TyreCompound.SOFT: -1.0,    # Fastest
            TyreCompound.MEDIUM: 0.0,   # Neutral
            TyreCompound.HARD: 0.8,     # Slowest
            TyreCompound.INTERMEDIATE: 2.0,  # Very slow on dry
            TyreCompound.WET: 4.0,      # Extremely slow on dry
        }
        return speed_modifiers.get(state.tyre_compound, 0.0)

    def _calculate_penalties(self, state: RaceState) -> float:
        """Calculate penalties for invalid strategies"""
        penalty = 0.0

        # Must pit at least once
        if state.pit_stops_made < 1:
            penalty += 100.0

        # Too many pit stops
        elif state.pit_stops_made > 3:
            penalty += 50.0 * (state.pit_stops_made - 3)

        return penalty
