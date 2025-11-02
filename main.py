"""
Main entry point for F1 Strategy Evolution

Author: Aleksandar Zekovic
"""

import random
import argparse
from src.evolution import GeneticAlgorithm
from src.utils import print_header, print_strategy_results, test_scenarios, plot_fitness_history


def main():
    """Main function to run F1 strategy evolution"""

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Evolve F1 Race Strategy using Genetic Programming')
    parser.add_argument('--population', type=int, default=50, help='Population size (default: 50)')
    parser.add_argument('--generations', type=int, default=100, help='Number of generations (default: 100)')
    parser.add_argument('--laps', type=int, default=50, help='Race laps (default: 50)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed (default: 42)')
    parser.add_argument('--no-tree', action='store_true', help='Hide decision tree visualization')
    args = parser.parse_args()

    # Set random seed for reproducibility
    random.seed(args.seed)

    # Print header
    print_header()

    # Create and configure genetic algorithm
    ga = GeneticAlgorithm(
        population_size=args.population,
        elite_size=5,
        tournament_size=3,
        mutation_rate=0.2,
        total_laps=args.laps
    )

    # Initialize population
    ga.initialize_population()

    # Run evolution
    best_strategy = ga.evolve(generations=args.generations, verbose=True)

    # Display results
    print_strategy_results(best_strategy, show_tree=not args.no_tree)

    # Test in different scenarios
    test_scenarios(best_strategy)

    # Plot fitness history
    plot_fitness_history(ga.fitness_history)


if __name__ == "__main__":
    main()
