"""
Visualization and output utilities
"""

from typing import List, Tuple
from ..models import RaceState, TyreCompound
from ..strategy import StrategyProgram


def print_header():
    """Print application header"""
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "🏎️  FORMULA 1 STRATEGY EVOLUTION 🏎️" + " " * 16 + "║")
    print("║" + " " * 10 + "Genetic Programming for Race Strategy" + " " * 20 + "║")
    print("║" + " " * 15 + "Author: Aleksandar Zekovic" + " " * 27 + "║")
    print("╚" + "═" * 68 + "╝")
    print()


def print_strategy_results(strategy: StrategyProgram, show_tree: bool = True):
    """Print evolved strategy results"""
    print("\n" + "═" * 70)
    print("🏆 BEST EVOLVED STRATEGY:")
    print("═" * 70)
    print()

    if show_tree:
        print(strategy.visualize())
    else:
        print("(Tree visualization hidden for brevity)")

    print()
    print(f"⏱️  Average race time: {strategy.fitness:.2f} seconds")
    print()


def test_scenarios(strategy: StrategyProgram):
    """Test strategy in different race scenarios"""
    print("\n" + "═" * 70)
    print("🧪 TESTING STRATEGY IN DIFFERENT SCENARIOS:")
    print("═" * 70)

    scenarios = [
        (
            RaceState(10, 5, TyreCompound.SOFT, 3, 5.0, -2.0, False, 0.1, 0, 0.0),
            "🔴 Early race, good position, soft tyres"
        ),
        (
            RaceState(25, 18, TyreCompound.MEDIUM, 8, 15.0, 1.5, True, 0.2, 1, 0.0),
            "🟡 Mid-race, safety car deployed!"
        ),
        (
            RaceState(45, 30, TyreCompound.HARD, 5, 8.0, -1.0, False, 0.7, 1, 0.1),
            "⚪ Late race, rain approaching"
        ),
        (
            RaceState(5, 3, TyreCompound.SOFT, 15, 25.0, 3.0, False, 0.1, 0, 0.0),
            "🟠 Start, poor position"
        ),
        (
            RaceState(20, 15, TyreCompound.MEDIUM, 6, 10.0, 0.5, False, 0.8, 1, 0.6),
            "🟢 Mid-race, track is wet!"
        ),
    ]

    for state, description in scenarios:
        decision = strategy.make_decision(state)
        print(f"\n{description}")
        print(f"   Lap: {state.current_lap} | Position: {state.position} | "
              f"Tyre age: {state.tyre_age} | Wetness: {state.track_wetness:.1f}")
        print(f"   Current: {state.tyre_compound.compound_name} {state.tyre_compound.color}")
        print(f"   ➜ DECISION: {decision}")


def plot_fitness_history(fitness_history: List[float]):
    """Simple text-based fitness plot"""
    if not fitness_history:
        return

    print("\n" + "═" * 70)
    print("📈 FITNESS EVOLUTION:")
    print("═" * 70)

    # Show key milestones
    print(f"Generation   0: {fitness_history[0]:.2f}s")
    if len(fitness_history) > 25:
        print(f"Generation  25: {fitness_history[25]:.2f}s")
    if len(fitness_history) > 50:
        print(f"Generation  50: {fitness_history[50]:.2f}s")
    if len(fitness_history) > 75:
        print(f"Generation  75: {fitness_history[75]:.2f}s")
    print(f"Generation {len(fitness_history)-1:3d}: {fitness_history[-1]:.2f}s")

    improvement = fitness_history[0] - fitness_history[-1]
    improvement_pct = (improvement / fitness_history[0]) * 100
    print(f"\n💪 Total improvement: {improvement:.2f}s ({improvement_pct:.2f}%)")
