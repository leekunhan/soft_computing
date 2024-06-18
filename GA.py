import numpy as np

def fitness_function(x):
    """簡單的適應度函數，用於評估個體的適應度。這裡我們嘗試最大化函數 f(x) = x^2"""
    return x**2

def initialize_population(size, x_min, x_max):
    """初始化群體"""
    return np.random.randint(x_min, x_max, size=size)

def selection(population, fitness, num_parents):
    """選擇操作：根據適應度選擇最好的個體作為父代"""
    indices = np.argsort(-fitness)
    return population[indices][:num_parents]

def crossover(parents, offspring_size):
    """交叉操作：從父代中創建後代"""
    offspring = np.empty(offspring_size)
    crossover_point = np.uint8(offspring_size[1] / 2)

    for k in range(offspring_size[0]):
        # 選擇父母
        parent1_idx = k % parents.shape[0]
        parent2_idx = (k + 1) % parents.shape[0]
        # 單點交叉
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

def mutation(offspring_crossover):
    """突變操作：對後代的基因進行隨機突變"""
    for idx in range(offspring_crossover.shape[0]):
        mutation_idx = np.random.randint(0, offspring_crossover.shape[1])
        offspring_crossover[idx, mutation_idx] = np.random.randint(-10, 10)
    return offspring_crossover

# 演算法參數
sol_per_pop = 8 # 群體中的解數量
num_parents_mating = 4 # 參與交配的父代數量
num_generations = 5 # 世代數
gene_length = 1 # 基因的長度

# 初始化群體
population = initialize_population(sol_per_pop, -10, 10)
print("Initial population:\n", population)

# 開始遺傳演算法
for generation in range(num_generations):
    # 評估適應度
    fitness = fitness_function(population)
    print("Fitness at generation", generation, ":", fitness)
    
    # 選擇最好的個體作為父代
    parents = selection(population, fitness, num_parents_mating)
    
    # 生成後代
    offspring_crossover = crossover(parents,
                                    (sol_per_pop - parents.shape[0], gene_length))
    
    # 突變後代
    offspring_mutation = mutation(offspring_crossover)
    
    # 新的群體
    population[0:parents.shape[0], :] = parents
    population[parents.shape[0]:, :] = offspring_mutation

# 輸出最終結果
fitness_last_gen = fitness_function(population)
best_match_idx = np.argmax(fitness_last_gen)
print("Best solution:", population[best_match_idx, :])
print("Best solution fitness:", fitness_last_gen[best_match_idx])
