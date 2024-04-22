import numpy as np

def pso(func, dim, bounds, num_particles=30, max_iter=100):
    # Initialize particles
    particles = np.random.rand(num_particles, dim) * (bounds[1] - bounds[0]) + bounds[0]
    p_best = particles.copy()
    p_best_scores = np.array([func(p) for p in particles])
    g_best = particles[np.argmin(p_best_scores)]

    velocity = np.zeros((num_particles, dim))
    for t in range(max_iter):
        r1, r2 = np.random.rand(2, num_particles, dim)
        velocity = 0.7 * velocity + 1.5 * r1 * (p_best - particles) + 2.0 * r2 * (g_best - particles)
        particles += velocity
        particles = np.clip(particles, bounds[0], bounds[1])

        fitness = np.array([func(p) for p in particles])
        better_mask = fitness < p_best_scores
        p_best[better_mask] = particles[better_mask]
        p_best_scores[better_mask] = fitness[better_mask]

        if min(fitness) < func(g_best):
            g_best = particles[np.argmin(fitness)]

    return g_best, func(g_best)