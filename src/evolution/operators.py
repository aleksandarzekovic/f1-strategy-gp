"""
Genetic operators: selection, crossover, mutation
"""

import random
import copy
from typing import List, Tuple
from ..strategy import StrategyProgram, StrategyNode
from ..models import Decision, TyreCompound


def tournament_selection(population: List[StrategyProgram], tournament_size: int) -> StrategyProgram:
    """Select a program using tournament selection"""
    tournament = random.sample(population, tournament_size)
    return min(tournament, key=lambda p: p.fitness)


def crossover(parent1: StrategyProgram, parent2: StrategyProgram) -> Tuple[StrategyProgram, StrategyProgram]:
    """Crossover two strategy trees by swapping subtrees"""
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

    # Swap random subtrees
    if random.random() < 0.7:
        node1 = _get_random_node(child1.decision_tree)
        node2 = _get_random_node(child2.decision_tree)

        if node1 and node2:
            # Swap left subtrees
            node1.left, node2.left = node2.left, node1.left

    return child1, child2


def mutate(program: StrategyProgram, mutation_rate: float):
    """Mutate strategy by changing conditions or actions"""
    _mutate_node(program.decision_tree, mutation_rate, program.CONDITIONS_POOL)


def _get_random_node(node: StrategyNode, depth: int = 0, max_depth: int = 3) -> StrategyNode:
    """Get random node from tree"""
    if node is None or depth >= max_depth or random.random() < 0.3:
        return node

    if random.random() < 0.5 and node.left:
        return _get_random_node(node.left, depth + 1, max_depth)
    elif node.right:
        return _get_random_node(node.right, depth + 1, max_depth)

    return node


def _mutate_node(node: StrategyNode, mutation_rate: float, conditions_pool: List[str], depth: int = 0):
    """Recursively mutate nodes in tree"""
    if node is None or random.random() > mutation_rate:
        return

    if node.node_type == 'action' and random.random() < 0.5:
        # Mutate action
        node.decision_value = Decision(
            pit_now=random.choice([True, False]),
            target_compound=random.choice(list(TyreCompound)),
            aggressive_pace=random.choice([True, False])
        )
    elif node.node_type == 'condition' and random.random() < 0.3:
        # Mutate condition
        node.condition = random.choice(conditions_pool)

    # Recurse to children
    if node.left:
        _mutate_node(node.left, mutation_rate, conditions_pool, depth + 1)
    if node.right:
        _mutate_node(node.right, mutation_rate, conditions_pool, depth + 1)
