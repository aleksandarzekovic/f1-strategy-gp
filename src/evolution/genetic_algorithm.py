"""
Main genetic algorithm engine
"""

from typing import List
from ..strategy import StrategyProgram
from ..simulation import RaceSimulator
from .operators import tournament_selection, crossover, mutate


class GeneticAlgorithm:
    """Main GP system for evolving F1 strategy"""

    def __init__(
        self,
        population_size: int = 50,
        elite_size: int = 5,
        tournament_size: int = 3,
        mutation_rate: float = 0.2,
        total_laps: int = 50
    ):
        self.population_size = population_size
        self.elite_size = elite_size
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate

        self.population: List[StrategyProgram] = []
        self.simulator = RaceSimulator(total_laps=total_laps)
        self.generation = 0
        self.best_strategy = None
        self.fitness_history = []

    def initialize_population(self):
        """Create initial population"""
        print("🏁 Creating initial population of strategies...")
        self.population = [StrategyProgram() for _ in range(self.population_size)]

        # Evaluate all
        for program in self.population:
            program.fitness = self._evaluate_strategy(program)

    def _evaluate_strategy(self, strategy: StrategyProgram) -> float:
        """Evaluate strategy through multiple races"""
        scores = []
        for _ in range(3):  # Average of 3 races
            score = self.simulator.simulate_race(strategy)
            scores.append(score)
        return sum(scores) / len(scores)

    def evolve(self, generations: int = 100, verbose: bool = True):
        """Run evolutionary algorithm"""
        if verbose:
            print(f"\n🏎️  Starting F1 strategy evolution!")
            print(f"Population: {self.population_size} | Generations: {generations}\n")

        for gen in range(generations):
            self.generation = gen

            # Sort by fitness
            self.population.sort(key=lambda p: p.fitness)
            self.best_strategy = self.population[0]
            self.fitness_history.append(self.best_strategy.fitness)

            # Progress report
            if verbose and gen % 10 == 0:
                best_time = self.best_strategy.fitness
                avg_time = sum(p.fitness for p in self.population[:10]) / 10
                print(f"Gen {gen:3d} | 🏆 Best: {best_time:.1f}s | "
                      f"📊 Top 10 avg: {avg_time:.1f}s")

            # Create new generation
            new_population = self._create_new_generation()
            self.population = new_population

        if verbose:
            print(f"\n✅ Evolution complete!\n")

        return self.best_strategy

    def _create_new_generation(self) -> List[StrategyProgram]:
        """Create new generation through selection, crossover, mutation"""
        new_population = []

        # Elitism - keep best
        new_population.extend(self.population[:self.elite_size])

        # Create offspring
        while len(new_population) < self.population_size:
            parent1 = tournament_selection(self.population, self.tournament_size)
            parent2 = tournament_selection(self.population, self.tournament_size)

            child1, child2 = crossover(parent1, parent2)

            mutate(child1, self.mutation_rate)
            mutate(child2, self.mutation_rate)

            child1.fitness = self._evaluate_strategy(child1)
            child2.fitness = self._evaluate_strategy(child2)

            new_population.extend([child1, child2])

        return new_population[:self.population_size]

    def get_best_strategy(self) -> StrategyProgram:
        """Return the best strategy found"""
        return self.best_strategy
