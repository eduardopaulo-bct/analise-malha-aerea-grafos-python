# Análise de Malha Aérea e Caminho Mínimo com Grafos em Python

Projeto acadêmico desenvolvido em grupo na **UFABC** (disciplina de Comunicação e Redes) por **Paulo Eduardo**, **Sophia Dumette** e **Eduardo Fernandez**, modelando e analisando a malha operacional de rotas aéreas da **Mandarin Airlines (`AE`)**[cite: 3, 4, 5].

## O que o projeto faz

- **`tarefa1.py`**: limpa e cruza os dados de `airports.dat` e `routes.dat` com **Pandas**, filtra a companhia aérea `AE`, calcula a distância geodésica em km entre aeroportos usando a fórmula de Haversine e gera a visualização do grafo completo com **NetworkX** e **Matplotlib**[cite: 5].
- **`tarefa2.py`**: constrói o grafo ponderado da rede e extrai indicadores estruturais, incluindo grau médio, conectividade de vértices, conectividade de arestas, excentricidade dos nós e diâmetro ponderado[cite: 4].
- **`tarefa3.py`**: calcula o caminho mínimo entre dois códigos IATA informados pelo usuário usando o algoritmo de **Dijkstra** e salva o destaque visual da rota em imagem[cite: 3].

## Bibliotecas utilizadas

- `pandas`[cite: 3, 4, 5]
- `networkx`[cite: 3, 4, 5]
- `matplotlib`[cite: 3, 5]
