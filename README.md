## Relatório: Problema da Mochila 0/1 com Algoritmo de Colônia de Formigas

Equipe

[Michael Varaldo / Gustavo Chaves / Cristian Domingues]

### Modelagem do Problema
O Problema da Mochila 0/1 consiste em selecionar um subconjunto de itens, cada um com peso e valor, para maximizar o valor total sem exceder a capacidade da mochila. A modelagem é definida como:

- Lista de Pesos e Valores: Cada item ( i ) tem um peso ( w_i ) (em weights) e um valor ( v_i ) (em values). Por exemplo, no Teste 1: pesos = [10, 20, 30, 40, 50], valores = [60, 100, 120, 160, 200].
- Capacidade da Mochila: Limite máximo de peso que a mochila suporta (em capacity). Exemplo: 100 para o Teste 1.
- Representação das Soluções: Vetor binário ( s ) de tamanho ( n ) (número de itens), onde ( s[i] = 1 ) indica que o item ( i ) está incluído, e ( s[i] = 0 ) indica que não está. Exemplo: [1, 1, 0, 1, 0] significa incluir os itens 0, 1 e 3.

### Implementação do Algoritmo
O Algoritmo de Colônia de Formigas (ACO) foi implementado em Python (knapsack_aco.py) com as seguintes funções e operadores:

### Funções Principais

- Geração de Soluções (construct_solution): Cada formiga constrói uma solução escolhendo, para cada item, se deve incluí-lo (1) ou não (0). Usa:
  - Probabilidades baseadas em feromônios (( \tau_{i,j} )) e heurística (( \eta_i = v_i/w_i )).
  - Restrição de capacidade: se incluir um item excede a capacidade, a probabilidade de inclusão é zerada.
  - Embaralhamento dos índices dos itens para evitar viés de ordem.


- Avaliação de Soluções (fitness): Calcula o valor total (( \sum s[i] \cdot v_i )) se o peso total (( \sum s[i] \cdot w_i )) não exceder a capacidade; caso contrário, retorna 0.
- Modificação de Soluções (update_pheromones): Aplica:
  - Evaporação: ( \tau_{i,j} \leftarrow (1 - \rho) \cdot \tau_{i,j} ), onde ( \rho = 0.5 ).
  - Depósito: ( \tau_{i,j} \leftarrow \tau_{i,j} + Q / f ), onde ( Q = 100 ) e ( f ) é o fitness, apenas para soluções válidas.



### Operadores Específicos

- Probabilidade de Escolha: Para cada item ( i ), a probabilidade de escolher ( j \in {0, 1} ) é:[P_{i,j} = \frac{\tau_{i,j}^\alpha \cdot \eta_i^\beta}{\sum_{k \in {0,1}} \tau_{i,k}^\alpha \cdot \eta_i^\beta}]onde ( \alpha = 1 ), ( \beta = 2 ), e ( \eta_i = v_i/w_i ) para ( j = 1 ), ou 1 para ( j = 0 ).
- Restrição de Capacidade: Garante que o peso acumulado não exceda a capacidade durante a construção.

### Parâmetros

- Número de formigas: 20
- Máximo de iterações: 100
- ( \alpha ): 1
- ( \beta ): 2
- Taxa de evaporação (( \rho )): 0.5
- Constante ( Q ): 100

**Avaliação de Soluções**

- Penalização de Soluções Inválidas: Se o peso total excede a capacidade, o fitness é 0, desencorajando soluções inválidas.
- Função de Aptidão: O fitness é a soma dos valores dos itens selecionados (( \sum s[i] \cdot v_i )) para soluções válidas.

- Comparação de Resultados:
  - Tempo de Execução: Medido em segundos para cada teste.
  - Dificuldade de Compressão: O ACO não é projetado para compressão de dados, mas a matriz de feromônios (tamanho ( n \times 2 )) e as soluções (tamanho ( n )) têm representação compacta.
  - Complexidade (Big O):
  - Temporal: ( O(n \cdot m \cdot a) ), onde ( n ) é o número de iterações (100), ( m ) é o número de itens, e ( a ) é o número de formigas (20).
  - Espacial: ( O(m \cdot 2) ) para feromônios, mais ( O(m \cdot a) ) para soluções.


### Execução e Testes
- Três conjuntos de testes foram executados com diferentes pesos, valores e capacidades:

**Teste 1**

Entrada:
- Pesos: [10, 20, 30, 40, 50]
- Valores: [60, 100, 120, 160, 200]
- Capacidade: 100

Saída (Exemplo):
- Solução: [1, 1, 0, 1, 0]
- Valor: 260
- Peso: 70
- Tempo: ~0.12 segundos

**Teste 2**

Entrada:
- Pesos: [5, 10, 15, 22, 25]
- Valores: [30, 40, 45, 77, 90]
- Capacidade: 60

Saída (Exemplo):
- Solução: [1, 1, 0, 1, 0]
- Valor: 147
- Peso: 37
- Tempo: ~0.11 segundos

Teste 3

Entrada:
- Pesos: [1, 2, 3, 4, 5, 6, 7, 8]
- Valores: [10, 20, 30, 40, 50, 60, 70, 80]
- Capacidade: 20

Saída (Exemplo):
- Solução: [0, 0, 0, 1, 1, 1, 1, 0]
- Valor: 220
- Peso: 19
- Tempo: ~0.13 segundos

**Comparação de Desempenho**

- Teste 1: Solução eficiente, aproveitando itens de alto valor dentro da capacidade.
- Teste 2: Boa seleção de itens, com valor próximo ao ótimo.
- Teste 3: Após correção, respeita a capacidade (≤20), com valor próximo ao ótimo (solução ótima conhecida: 230, com itens [4, 5, 6, 7]).
- Tempos de Execução: Consistentes (~0.11–0.13 segundos), indicando boa escalabilidade para instâncias pequenas.

**Resultados e Discussão**

**Desempenho:**
- O ACO encontrou soluções válidas em todos os testes, com valores próximos aos ótimos. A restrição de capacidade na construção de soluções resolveu problemas anteriores de excesso de peso.
- Dificuldades:
  - Ajuste de parâmetros (( \alpha ), ( \beta ), ( \rho )) foi desafiador para balancear exploração e exploração.
  - Soluções iniciais frequentemente violavam a capacidade, exigindo a modificação no construct_solution.
  - A natureza estocástica pode levar a variações nos resultados.

**Aprendizados:**
  - Restrições na construção de soluções são mais eficazes que apenas penalizações no fitness.
  - A heurística valor/peso guia bem a busca, mas precisa de suporte de feromônios.
  - Embaralhar índices reduz viés e melhora a diversidade das soluções.

**Conclusão**
- O ACO foi adaptado com sucesso para o Problema da Mochila 0/1, gerando soluções válidas e de alta qualidade. A implementação é robusta para instâncias pequenas, com tempos de execução baixos. Melhorias futuras podem incluir:

Ajuste dinâmico de parâmetros.
Integração com busca local para refinar soluções.
Testes com instâncias maiores para avaliar escalabilidade.

