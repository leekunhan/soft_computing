import numpy as np

class AntColonyOptimizer:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        ACO算法初始化
        :param distances: 距離矩陣
        :param n_ants: 螞蟻數量
        :param n_best: 每代考慮的最佳螞蟻數量
        :param n_iterations: 迭代次數
        :param decay: 信息素的蒸發率
        :param alpha: 信息素的影響因子
        :param beta: 啟發式信息的影響因子
        """
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        best_cost = float('inf')
        for i in range(self.n_iterations):
            all_paths = self.generate_paths()
            self.spread_pheromone(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < best_cost:
                best_cost = shortest_path[1]
                best_path = shortest_path
            self.pheromone * self.decay
        return best_path

    def spread_pheromone(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, cost in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def generate_paths(self):
        all_paths = []
        for _ in range(self.n_ants):
            path = self.generate_path(0)
            all_paths.append((path, self.path_cost(path)))
        return all_paths

    def generate_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for _ in range(len(self.distances) - 1):
            move = self.probable_next_step(prev, visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # returning to start point
        return path

    def probable_next_step(self, prev, visited):
        pheromone = np.power(self.pheromone[prev], self.alpha)
        heuristic = np.power(1.0 / self.distances[prev], self.beta)
        probabilities = pheromone * heuristic

        probabilities[list(visited)] = 0  # set probabilities of visited to zero
        probabilities = probabilities / probabilities.sum()
        next_step = np.random.choice(self.all_inds, 1, p=probabilities)[0]
        return next_step

    def path_cost(self, path):
        total_cost = 0
        for (start, end) in path:
            total_cost += self.distances[start][end]
        return total_cost

# Define a small 5-city distance matrix
distances = np.array([
    [0, 2, 2, 5, 7],
    [2, 0, 4, 8, 2],
    [2, 4, 0, 1, 3],
    [5, 8, 1, 0, 2],
    [7, 2, 3, 2, 0]
])

# Create an instance of the ACO
aco = AntColonyOptimizer(distances, n_ants=5, n_best=2, n_iterations=100, decay=0.95, alpha=1, beta=1)

# Run the ACO
best_path = aco.run()

# Print the best path and its cost
best_path
