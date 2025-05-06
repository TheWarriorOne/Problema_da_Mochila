import numpy as np
import time
import random

# Classe que implementa o Algoritmo de Colônia de Formigas para o Problema da Mochila 0/1
class KnapsackACO:
    # Inicializa os parâmetros do problema e do algoritmo
    def __init__(self, weights, values, capacity, num_ants=20, max_iterations=100, alpha=1, beta=2, evaporation_rate=0.5, q=100):
        self.weights = np.array(weights)  # Converte lista de pesos para array NumPy
        self.values = np.array(values)    # Converte lista de valores para array NumPy
        self.capacity = capacity          # Capacidade máxima da mochila
        self.num_items = len(weights)     # Número total de itens
        self.num_ants = num_ants          # Número de formigas por iteração
        self.max_iterations = max_iterations  # Número máximo de iterações
        self.alpha = alpha                # Influência do feromônio na escolha
        self.beta = beta                  # Influência da heurística na escolha
        self.evaporation_rate = evaporation_rate  # Taxa de evaporação do feromônio
        self.q = q                        # Constante para depósito de feromônio
        
        # Inicializa a matriz de feromônios com valor inicial 0.1
        # Dimensão: num_items x 2 (0 para não incluir, 1 para incluir)
        self.pheromones = np.ones((self.num_items, 2)) * 0.1
        
        # Calcula heurística como razão valor/peso para cada item
        self.heuristic = np.array([v/w for v, w in zip(values, weights)])
        
        self.best_solution = None         # Melhor solução encontrada
        self.best_fitness = -1            # Melhor valor (fitness) encontrado
        self.best_weight = 0              # Peso da melhor solução

    # Calcula o fitness de uma solução
    def fitness(self, solution):
        # Calcula o peso total da solução (soma de pesos dos itens selecionados)
        total_weight = np.sum(solution * self.weights)
        # Calcula o valor total da solução (soma de valores dos itens selecionados)
        total_value = np.sum(solution * self.values)
        
        # Penaliza soluções que excedem a capacidade da mochila
        if total_weight > self.capacity:
            return 0
        return total_value  # Retorna o valor total para soluções válidas

    # Constrói uma solução para uma formiga
    def construct_solution(self):
        # Inicializa vetor binário de solução (0 = não incluído, 1 = incluído)
        solution = np.zeros(self.num_items, dtype=int)
        # Vetor para armazenar probabilidades de incluir (1) ou não (0)
        probabilities = np.zeros(2)
        # Rastreia o peso acumulado da solução
        current_weight = 0
        
        # Embaralha índices dos itens para evitar viés de ordem
        indices = list(range(self.num_items))
        random.shuffle(indices)
        
        # Para cada item, decide se deve ser incluído
        for i in indices:
            # Verifica se incluir o item respeita a capacidade
            if current_weight + self.weights[i] <= self.capacity:
                # Calcula probabilidade de não incluir (baseada em feromônio)
                probabilities[0] = (self.pheromones[i, 0] ** self.alpha) * (1 ** self.beta)
                # Calcula probabilidade de incluir (baseada em feromônio e heurística)
                probabilities[1] = (self.pheromones[i, 1] ** self.alpha) * (self.heuristic[i] ** self.beta)
            else:
                # Se exceder a capacidade, força a não inclusão
                probabilities[0] = 1.0
                probabilities[1] = 0.0
            
            # Normaliza probabilidades para soma igual a 1
            probabilities /= np.sum(probabilities) + 1e-10  # Evita divisão por zero
            # Escolhe aleatoriamente com base nas probabilidades
            choice = np.random.choice([0, 1], p=probabilities)
            solution[i] = choice
            # Atualiza peso acumulado se o item for incluído
            if choice == 1:
                current_weight += self.weights[i]
        
        return solution  # Retorna a solução construída

    # Atualiza os níveis de feromônio
    def update_pheromones(self, solutions, fitnesses):
        # Aplica evaporação a todos os feromônios
        self.pheromones *= (1 - self.evaporation_rate)
        
        # Deposita feromônio com base nas soluções válidas
        for solution, fitness in zip(solutions, fitnesses):
            if fitness > 0:  # Apenas para soluções válidas (fitness > 0)
                for i in range(self.num_items):
                    # Adiciona feromônio proporcional ao inverso do fitness
                    self.pheromones[i, solution[i]] += self.q / fitness

    # Executa o algoritmo ACO
    def run(self):
        # Registra o tempo inicial para medir a execução
        start_time = time.time()
        
        # Executa o número especificado de iterações
        for iteration in range(self.max_iterations):
            solutions = []  # Lista para armazenar soluções das formigas
            fitnesses = []  # Lista para armazenar fitness das soluções
            
            # Cada formiga constrói uma solução
            for _ in range(self.num_ants):
                solution = self.construct_solution()
                fitness = self.fitness(solution)
                solutions.append(solution)
                fitnesses.append(fitness)
                
                # Atualiza a melhor solução encontrada
                if fitness > self.best_fitness:
                    self.best_fitness = fitness
                    self.best_solution = solution.copy()
                    self.best_weight = np.sum(solution * self.weights)
            
            # Atualiza os feromônios com base nas soluções
            self.update_pheromones(solutions, fitnesses)
        
        # Calcula o tempo total de execução
        execution_time = time.time() - start_time
        # Retorna a melhor solução, seu valor, peso e tempo de execução
        return self.best_solution, self.best_fitness, self.best_weight, execution_time

# Função para testar o algoritmo com diferentes conjuntos de dados
def test_knapsack():
    # Define três casos de teste com pesos, valores e capacidades
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
    
    results = []  # Lista para armazenar resultados dos testes
    # Executa o algoritmo para cada caso de teste
    for i, test in enumerate(test_cases):
        # Inicializa o ACO com os parâmetros do teste
        aco = KnapsackACO(test['weights'], test['values'], test['capacity'])
        # Executa o algoritmo e obtém resultados
        solution, value, weight, exec_time = aco.run()
        # Armazena resultados em um dicionário
        results.append({
            'test_case': i + 1,
            'solution': solution.tolist(),
            'value': value,
            'weight': weight,
            'execution_time': exec_time
        })
    
    return results  # Retorna a lista de resultados

# Bloco principal para executar os testes e exibir resultados
if __name__ == "__main__":
    # Executa os testes
    results = test_knapsack()
    # Exibe os resultados de cada teste
    for result in results:
        print(f"\nTeste {result['test_case']}:")
        print(f"Solução: {result['solution']}")
        print(f"Valor: {result['value']}")
        print(f"Peso: {result['weight']}")
        print(f"Tempo de execução: {result['execution_time']:.4f} segundos")
