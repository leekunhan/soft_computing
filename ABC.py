import numpy as np

def abc(func, dim, bounds, num_bees=30, max_iter=100):
    def generate_new_point(x, partner):
        phi = np.random.uniform(-1, 1, size=len(x))
        new_x = x + phi * (x - partner)
        return np.clip(new_x, bounds[0], bounds[1])

    # Initialize population
    population = np.random.rand(num_bees, dim) * (bounds[1] - bounds[0]) + bounds[0]
    fitness = np.array([func(individual) for individual in population])
    trial_counters = np.zeros(num_bees)

    for _ in range(max_iter):
        # Employed bee phase
        for i in range(num_bees):
            partner_idx = np.random.randint(0, num_bees)
            while partner_idx == i:
                partner_idx = np.random.randint(0, num_bees)
            new_solution = generate_new_point(population[i], population[partner_idx])
            new_fitness = func(new_solution)
            if new_fitness < fitness[i]:
                population[i] = new_solution
                fitness[i] = new_fitness
                trial_counters[i] = 0
            else:
                trial_counters[i] += 1

        # Calculate probabilities
        fitness_max = np.max(fitness)
        probabilities = (fitness_max - fitness) / (fitness_max - np.min(fitness))

        # Onlooker bee phase
        for i in range(num_bees):
            if np.random.rand() < probabilities[i]:
                partner_idx = np.random.randint(0, num_bees)
                new_solution = generate_new_point(population[i], population[partner_idx])
                new_fitness = func(new_solution)
                if new_fitness < fitness[i]:
                    population[i] = new_solution
                    fitness[i] = new_fitness
                    trial_counters[i] = 0
                else:
                    trial_counters[i] += 1

        # Scout bee phase
        for i in range(num_bees):
            if trial_counters[i] > 5:
                population[i] = np.random.rand(dim) * (bounds[1] - bounds[0]) + bounds[0]
                fitness[i] = func(population[i])
                trial_counters[i] = 0

    best_idx = np.argmin(fitness)
    return population[best_idx], fitness[best_idx]