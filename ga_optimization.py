import random
import numpy as np
from yp import LINE_CAPACITY, LINE_CLEANING_TIME, TOTAL_TIME_LIMIT, PRODUCTION_PLAN, gantt_data, draw_gantt_chart

LINES = list(LINE_CAPACITY.keys())
YOGURTS = list(PRODUCTION_PLAN.keys())
POPULATION_SIZE = 30
GENERATIONS = 300
MUTATION_RATE = 0.2

# For dynamic parameter optimization
_current_population_size = POPULATION_SIZE
_current_generations = GENERATIONS
_current_mutation_rate = MUTATION_RATE

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

def mutate(individual, mutation_rate=None):
    if mutation_rate is None:
        mutation_rate = _current_mutation_rate
    new_ind = individual.copy()
    if random.random() < mutation_rate:
        idx = random.randint(0, len(new_ind) - 1)
        new_ind[idx] = random.choice(LINES)
    return new_ind

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 2)
    return parent1[:point] + parent2[point:]

def genetic_algorithm(population_size=None, generations=None, mutation_rate=None, verbose=True):
    global _current_population_size, _current_generations, _current_mutation_rate
    
    if population_size is None:
        population_size = _current_population_size
    if generations is None:
        generations = _current_generations
    if mutation_rate is None:
        mutation_rate = _current_mutation_rate
    
    _current_population_size = population_size
    _current_generations = generations
    _current_mutation_rate = mutation_rate
    
    population = [generate_individual() for _ in range(population_size)]
    for generation in range(generations):
        scores = [(simulate_plan(ind), ind) for ind in population]
        scores.sort()
        population = [ind for _, ind in scores[:population_size // 2]]

        while len(population) < population_size:
            p1, p2 = random.sample(population[:max(1, population_size // 4)], 2)
            child = mutate(crossover(p1, p2), mutation_rate)
            population.append(child)

        if verbose:
            print(f"Generation {generation + 1}: best time = {scores[0][0]:.2f}")

    best_time, best_individual = min((simulate_plan(ind), ind) for ind in population)
    return best_individual, best_time

def optimize_hyperparameters(num_trials=10):
    """
    Tries different combinations of GA parameters to find the best setup.
    """
    print("=== Hyperparameter Optimization (Random Search) ===\n")
    
    # Define parameter ranges to try
    population_sizes = [20, 30, 50, 100]
    generation_counts = [100, 200, 300, 500]
    mutation_rates = [0.1, 0.2, 0.3, 0.5]
    
    results = []
    
    for trial in range(num_trials):
        pop_size = random.choice(population_sizes)
        gens = random.choice(generation_counts)
        mut_rate = random.choice(mutation_rates)
        
        print(f"\nTrial {trial + 1}/{num_trials}:")
        print(f"  Population: {pop_size}, Generations: {gens}, Mutation Rate: {mut_rate}")
        
        try:
            best_plan, best_time = genetic_algorithm(
                population_size=pop_size,
                generations=gens,
                mutation_rate=mut_rate,
                verbose=False
            )
            
            print(f"  Result: {best_time:.2f} hours")
            results.append({
                'population_size': pop_size,
                'generations': gens,
                'mutation_rate': mut_rate,
                'best_time': best_time,
                'best_plan': best_plan
            })
        except Exception as e:
            print(f"  Failed: {e}")
    
    # Find best configuration
    results.sort(key=lambda x: x['best_time'])
    best_config = results[0]
    
    print("\n" + "="*50)
    print("=== BEST CONFIGURATION FOUND ===")
    print(f"Population Size: {best_config['population_size']}")
    print(f"Generations: {best_config['generations']}")
    print(f"Mutation Rate: {best_config['mutation_rate']}")
    print(f"Best Time: {best_config['best_time']:.2f} hours")
    print("="*50)
    
    return best_config

def evolutionary_hyperparameter_optimization(meta_pop_size=10, meta_generations=5):
    """
    Uses an evolutionary algorithm to find the best hyperparameters.
    Each individual represents a set of GA hyperparameters.
    """
    print("=== Evolutionary Hyperparameter Optimization ===\n")
    print(f"Meta-GA: Population={meta_pop_size}, Generations={meta_generations}\n")
    
    # Parameter bounds
    POP_MIN, POP_MAX = 20, 100
    GEN_MIN, GEN_MAX = 100, 500
    MUT_MIN, MUT_MAX = 0.1, 0.5
    
    def generate_meta_individual():
        """Generate random hyperparameter set"""
        return {
            'population_size': random.randint(POP_MIN, POP_MAX),
            'generations': random.randint(GEN_MIN, GEN_MAX),
            'mutation_rate': round(random.uniform(MUT_MIN, MUT_MAX), 2)
        }
    
    def evaluate_meta_individual(params):
        """Evaluate a hyperparameter set by running the GA"""
        try:
            _, best_time = genetic_algorithm(
                population_size=params['population_size'],
                generations=params['generations'],
                mutation_rate=params['mutation_rate'],
                verbose=False
            )
            return best_time
        except Exception as e:
            return float('inf')
    
    def mutate_meta_individual(params):
        """Mutate hyperparameters"""
        new_params = params.copy()
        mutation_type = random.choice(['pop', 'gen', 'mut'])
        
        if mutation_type == 'pop':
            delta = random.randint(-20, 20)
            new_params['population_size'] = max(POP_MIN, min(POP_MAX, params['population_size'] + delta))
        elif mutation_type == 'gen':
            delta = random.randint(-100, 100)
            new_params['generations'] = max(GEN_MIN, min(GEN_MAX, params['generations'] + delta))
        else:  # mut
            delta = random.uniform(-0.1, 0.1)
            new_params['mutation_rate'] = max(MUT_MIN, min(MUT_MAX, round(params['mutation_rate'] + delta, 2)))
        
        return new_params
    
    def crossover_meta_individuals(parent1, parent2):
        """Crossover two hyperparameter sets"""
        child = {}
        for key in parent1:
            child[key] = parent1[key] if random.random() < 0.5 else parent2[key]
        return child
    
    # Initialize population
    print("Initializing meta-population...")
    meta_population = [generate_meta_individual() for _ in range(meta_pop_size)]
    
    best_overall = None
    best_overall_fitness = float('inf')
    
    # Evolution loop
    for gen in range(meta_generations):
        print(f"\n{'='*60}")
        print(f"META-GENERATION {gen + 1}/{meta_generations}")
        print('='*60)
        
        # Evaluate population
        fitness_scores = []
        for idx, individual in enumerate(meta_population):
            print(f"\n  Evaluating config {idx + 1}/{meta_pop_size}:")
            print(f"    Pop={individual['population_size']}, Gen={individual['generations']}, Mut={individual['mutation_rate']}")
            
            fitness = evaluate_meta_individual(individual)
            fitness_scores.append((fitness, individual))
            
            print(f"    → Fitness: {fitness:.2f} hours")
            
            if fitness < best_overall_fitness:
                best_overall_fitness = fitness
                best_overall = individual.copy()
        
        # Sort by fitness
        fitness_scores.sort(key=lambda x: x[0])
        
        print(f"\n  Best in generation: {fitness_scores[0][0]:.2f} hours")
        print(f"  Best overall: {best_overall_fitness:.2f} hours")
        
        # Selection: keep top 50%
        survivors = [ind for _, ind in fitness_scores[:meta_pop_size // 2]]
        
        # Generate new population
        new_population = survivors.copy()
        
        while len(new_population) < meta_pop_size:
            # Select parents from top performers
            parent1, parent2 = random.sample(survivors[:max(2, len(survivors)//2)], 2)
            
            # Crossover and mutate
            child = crossover_meta_individuals(parent1, parent2)
            if random.random() < 0.7:  # 70% mutation rate for meta-GA
                child = mutate_meta_individual(child)
            
            new_population.append(child)
        
        meta_population = new_population
    
    # Final results
    print("\n" + "="*60)
    print("=== BEST HYPERPARAMETERS FOUND (Evolutionary) ===")
    print(f"Population Size: {best_overall['population_size']}")
    print(f"Generations: {best_overall['generations']}")
    print(f"Mutation Rate: {best_overall['mutation_rate']}")
    print(f"Best Time Achieved: {best_overall_fitness:.2f} hours")
    print("="*60)
    
    return best_overall

if __name__ == "__main__":
    import sys
    
    best_config = None
    
    if len(sys.argv) > 1 and sys.argv[1] == '--optimize':
        # Run random search hyperparameter optimization
        num_trials = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        best_config = optimize_hyperparameters(num_trials)
        
        # Run final optimization with best parameters
        print("\n=== Running Final Optimization with Best Parameters ===")
        best_plan, time = genetic_algorithm(
            population_size=best_config['population_size'],
            generations=best_config['generations'],
            mutation_rate=best_config['mutation_rate'],
            verbose=True
        )
    elif len(sys.argv) > 1 and sys.argv[1] == '--evolve':
        # Run evolutionary hyperparameter optimization
        meta_pop = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        meta_gen = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        best_config = evolutionary_hyperparameter_optimization(meta_pop, meta_gen)
        
        # Run final optimization with best evolved parameters
        print("\n=== Running Final Optimization with Evolved Parameters ===")
        best_plan, time = genetic_algorithm(
            population_size=best_config['population_size'],
            generations=best_config['generations'],
            mutation_rate=best_config['mutation_rate'],
            verbose=True
        )
    else:
        # Standard run with default parameters
        best_plan, time = genetic_algorithm()
    
    print("\n" + "="*60)
    print("=== FINAL RESULTS ===")
    print("="*60)
    
    if best_config:
        print("\n*** Best Hyperparameters Used ***")
        print(f"  Population Size: {best_config['population_size']}")
        print(f"  Generations: {best_config['generations']}")
        print(f"  Mutation Rate: {best_config['mutation_rate']}")
    else:
        print("\n*** Default Hyperparameters Used ***")
        print(f"  Population Size: {POPULATION_SIZE}")
        print(f"  Generations: {GENERATIONS}")
        print(f"  Mutation Rate: {MUTATION_RATE}")
    
    print(f"\n*** Optimization Result ***")
    print(f"  Best Time: {time:.2f} hours")
    
    print("\n*** Production Plan ***")
    from yp import PRODUCTION_PLAN
    plan_dict = {yogurt: line for yogurt, line in zip(PRODUCTION_PLAN.keys(), best_plan)}
    for yogurt, line in plan_dict.items():
        print(f"  {yogurt:15s} → {line}")
    
    print("\n" + "="*60)
    
    simulate_plan(best_plan)
    draw_gantt_chart()
