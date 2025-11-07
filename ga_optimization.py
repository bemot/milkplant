import random
import numpy as np
from yp import LINE_CAPACITY, LINE_CLEANING_TIME, TOTAL_TIME_LIMIT, PRODUCTION_PLAN, gantt_data, draw_gantt_chart

LINES = list(LINE_CAPACITY.keys())
YOGURTS = list(PRODUCTION_PLAN.keys())
POPULATION_SIZE = 30
GENERATIONS = 300
MUTATION_RATE = 0.2

def generate_individual():
    return [random.choice(LINES) for _ in YOGURTS]

def decode_plan(individual):
    plan = {line: [] for line in LINES}
    for yogurt, line in zip(YOGURTS, individual):
        plan[line].append(yogurt)
    return plan

def simulate_plan(individual):
    plan = decode_plan(individual)
    end_times = {line: 0 for line in LINES}
    last_type = {line: None for line in LINES}
    gantt_data.clear()

    for line, yogurts in plan.items():
        for yogurt in yogurts:
            qty = PRODUCTION_PLAN[yogurt]
            cleaning_needed = last_type[line] and last_type[line] != yogurt
            cleaning_time = LINE_CLEANING_TIME[line] if cleaning_needed else 0
            start = end_times[line] + cleaning_time
            available_time = TOTAL_TIME_LIMIT - start
            if available_time <= 0:
                return float('inf')

            duration = qty / LINE_CAPACITY[line]
            end = start + duration
            if end > TOTAL_TIME_LIMIT:
                return float('inf')

            gantt_data.append((line, start, end, yogurt))
            end_times[line] = end
            last_type[line] = yogurt

    return max(end_times.values())

def mutate(individual):
    new_ind = individual.copy()
    if random.random() < MUTATION_RATE:
        idx = random.randint(0, len(new_ind) - 1)
        new_ind[idx] = random.choice(LINES)
    return new_ind

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 2)
    return parent1[:point] + parent2[point:]

def genetic_algorithm():
    population = [generate_individual() for _ in range(POPULATION_SIZE)]
    for generation in range(GENERATIONS):
        scores = [(simulate_plan(ind), ind) for ind in population]
        scores.sort()
        population = [ind for _, ind in scores[:POPULATION_SIZE // 2]]

        while len(population) < POPULATION_SIZE:
            p1, p2 = random.sample(population[:POPULATION_SIZE // 4], 2)
            child = mutate(crossover(p1, p2))
            population.append(child)

        print(f"Generation {generation + 1}: best time = {scores[0][0]:.2f}")

    best_time, best_individual = min((simulate_plan(ind), ind) for ind in population)
    return best_individual, best_time

if __name__ == "__main__":
    best_plan, time = genetic_algorithm()
    print("\n=== Best Plan Found ===")
    from yp import PRODUCTION_PLAN
    print({yogurt: line for yogurt, line in zip(PRODUCTION_PLAN.keys(), best_plan)})
    simulate_plan(best_plan)
    draw_gantt_chart()
