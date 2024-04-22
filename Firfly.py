def firefly_algorithm(func, dim, bounds, num_fireflies=30, max_iter=100, absorption=1.0):
    def attractiveness(brightness, distance, gamma):
        return brightness * np.exp(-gamma * (distance ** 2))

    # Initialize fireflies
    fireflies = np.random.rand(num_fireflies, dim) * (bounds[1] - bounds[0]) + bounds[0]
    brightness = np.array([-func(firefly) for firefly in fireflies])

    for _ in range(max_iter):
        for i in range(num_fireflies):
            for j in range(num_fireflies):
                if brightness[j] > brightness[i]:
                    distance = np.linalg.norm(fireflies[i] - fireflies[j])
                    beta = attractiveness(brightness[j], distance, absorption)
                    step = beta * (fireflies[j] - fireflies[i])
                    new_position = fireflies[i] + step + np.random.uniform(-0.1, 0.1, dim)
                    fireflies[i] = np.clip(new_position, bounds[0], bounds[1])
                    new_brightness = -func(fireflies[i])
                    if new_brightness > brightness[i]:
                        brightness[i] = new_brightness

    best_idx = np.argmax(brightness)
    return fireflies[best_idx], -brightness[best_idx]