import numpy as np
import time
import random

class KnapsackACO:
    def __init__(self, weights, values, capacity, num_ants=20, max_iterations=100, alpha=1, beta=2, evaporation_rate=0.5, q=100):
        self.weights = np.array(weights)
        self.values = np.array(values)
        self.capacity = capacity
        self.num_items = len(weights)
        self.num_ants = num_ants
        self.max_iterations = max_iterations
        self.alpha = alpha  # Influência do feromônio
        self.beta = beta   # Influência da heurística
        self.evaporation_rate = evaporation_rate
        self.q = q  # Constante de depósito de feromônio
        
        # Inicializar feromônios
        self.pheromones = np.ones((self.num_items, 2)) * 0.1  # 2 opções por item: incluir (1) ou não (0)
        
        # Informações heurísticas baseadas no valor/peso
        self.heuristic = np.array([v/w for v, w in zip(values, weights)])
        
        self.best_solution = None
        self.best_fitness = -1
        self.best_weight = 0

    def fitness(self, solution):
        total_weight = np.sum(solution * self.weights)
        total_value = np.sum(solution * self.values)
        
        # Penalizar soluções inválidas
        if total_weight > self.capacity:
            return 0
        return total_value

    def construct_solution(self):
        solution = np.zeros(self.num_items, dtype=int)
        probabilities = np.zeros(2)  # Probabilidades para incluir (1) ou não (0)
        current_weight = 0
        
        # Embaralhar índices para evitar viés de ordem
        indices = list(range(self.num_items))
        random.shuffle(indices)
        
        for i in indices:
            # Verificar se incluir o item excede a capacidade
            if current_weight + self.weights[i] <= self.capacity:
                # Calcular probabilidades com base em feromônio e heurística
                probabilities[0] = (self.pheromones[i, 0] ** self.alpha) * (1 ** self.beta)
                probabilities[1] = (self.pheromones[i, 1] ** self.alpha) * (self.heuristic[i] ** self.beta)
            else:
                # Se exceder, forçar escolha de não incluir (0)
                probabilities[0] = 1.0
                probabilities[1] = 0.0
            
            probabilities /= np.sum(probabilities) + 1e-10  # Evitar divisão por zero
            choice = np.random.choice([0, 1], p=probabilities)
            solution[i] = choice
            if choice == 1:
                current_weight += self.weights[i]
        
        return solution

    def update_pheromones(self, solutions, fitnesses):
        # Evaporação
        self.pheromones *= (1 - self.evaporation_rate)
        
        # Depósito de feromônio
        for solution, fitness in zip(solutions, fitnesses):
            if fitness > 0:  # Apenas para soluções válidas
                for i in range(self.num_items):
                    self.pheromones[i, solution[i]] += self.q / fitness

    def run(self):
        start_time = time.time()
        
        for iteration in range(self.max_iterations):
            solutions = []
            fitnesses = []
            
            # Construir soluções para todas as formigas
            for _ in range(self.num_ants):
                solution = self.construct_solution()
                fitness = self.fitness(solution)
                solutions.append(solution)
                fitnesses.append(fitness)
                
                # Atualizar melhor solução
                if fitness > self.best_fitness:
                    self.best_fitness = fitness
                    self.best_solution = solution.copy()
                    self.best_weight = np.sum(solution * self.weights)
            
            # Atualizar feromônios
            self.update_pheromones(solutions, fitnesses)
        
        execution_time = time.time() - start_time
        return self.best_solution, self.best_fitness, self.best_weight, execution_time

def test_knapsack():
    test_cases = [
        {
            'weights': [10, 20, 30, 40, 50],
            'values': [60, 100, 120, 160, 200],
            'capacity': 100
        },
        {
            'weights': [5, 10, 15, 22, 25],
            'values': [30, 40, 45, 77, 90],
            'capacity': 60
        },
        {
            'weights': [1, 2, 3, 4, 5, 6, 7, 8],
            'values': [10, 20, 30, 40, 50, 60, 70, 80],
            'capacity': 20
        }
    ]
    
    results = []
    for i, test in enumerate(test_cases):
        aco = KnapsackACO(test['weights'], test['values'], test['capacity'])
        solution, value, weight, exec_time = aco.run()
        results.append({
            'test_case': i + 1,
            'solution': solution.tolist(),
            'value': value,
            'weight': weight,
            'execution_time': exec_time
        })
    
    return results

if __name__ == "__main__":
    results = test_knapsack()
    for result in results:
        print(f"\nTeste {result['test_case']}:")
        print(f"Solução: {result['solution']}")
        print(f"Valor: {result['value']}")
        print(f"Peso: {result['weight']}")
        print(f"Tempo de execução: {result['execution_time']:.4f} segundos")
