# Grupo 14 -: Paulo Eduardo , Sophia Dumette e Eduardo Fernandez
# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math

def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    raio_terrestre = 6371.0
    phi_1, phi_2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    termo_a = (math.sin(delta_phi / 2.0) ** 2 + 
               math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2)
    termo_c = 2.0 * math.atan2(math.sqrt(termo_a), math.sqrt(1.0 - termo_a))
    return raio_terrestre * termo_c

def main():
    df_aeroportos = pd.read_csv('airports.dat', header=None, 
                                names=['ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 
                                       'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz', 'Type', 'Source'])
    
    df_rotas = pd.read_csv('routes.dat', header=None,
                           names=['Airline', 'Airline_ID', 'Source_Airport', 'Source_Airport_ID', 
                                  'Dest_Airport', 'Dest_Airport_ID', 'Codeshare', 'Stops', 'Equipment'])

    voos_filtrados = df_rotas[df_rotas['Airline'] == 'AE'].copy()
    
    aeroportos_validos = df_aeroportos[
        df_aeroportos['IATA'].notna() & 
        (df_aeroportos['IATA'] != '\\N') & 
        (df_aeroportos['IATA'] != '')
    ].drop_duplicates(subset=['IATA'])
    
    mapa_coordenadas = aeroportos_validos.set_index('IATA')[['Name', 'Latitude', 'Longitude', 'City', 'Country']].to_dict('index')

    grafo_conexoes = nx.Graph()
    
    for _, registro in voos_filtrados.iterrows():
        orig, dest = registro['Source_Airport'], registro['Dest_Airport']
        if orig in mapa_coordenadas and dest in mapa_coordenadas:
            if orig == dest: 
                continue
            lt_o, lg_o = mapa_coordenadas[orig]['Latitude'], mapa_coordenadas[orig]['Longitude']
            lt_d, lg_d = mapa_coordenadas[dest]['Latitude'], mapa_coordenadas[dest]['Longitude']
            km_distancia = calcular_distancia_haversine(lt_o, lg_o, lt_d, lg_d)
            if not grafo_conexoes.has_edge(orig, dest):
                grafo_conexoes.add_edge(orig, dest, weight=km_distancia)

    aeroporto_origem = input("Código IATA de Origem: ").strip().upper()
    aeroporto_destino = input("Código IATA de Destino: ").strip().upper()
    
    if aeroporto_origem in grafo_conexoes and aeroporto_destino in grafo_conexoes:
        rota_calculada = nx.dijkstra_path(grafo_conexoes, source=aeroporto_origem, target=aeroporto_destino, weight='weight')
        distancia_total = nx.dijkstra_path_length(grafo_conexoes, source=aeroporto_origem, target=aeroporto_destino, weight='weight')
        
        print(f"\nCaminho Mínimo Encontrado: {' -> '.join(rota_calculada)}")
        print(f"Distância Total da Viagem: {distancia_total:.2f} km\n")
        
        plt.figure(figsize=(10, 8))
        posicionamento = nx.spring_layout(grafo_conexoes, k=1.5 / math.sqrt(len(grafo_conexoes.nodes())), iterations=150, seed=42)
        
        TONALIDADE_ROTA = '#e74c3c'
        TONALIDADE_PADRAO = '#2ecc71'
        TONALIDADE_CONEXAO = '#dfe6e9'
        
        vetor_cores_nos = []
        vetor_tamanhos_nos = []
        for no in grafo_conexoes.nodes():
            if no in rota_calculada:
                vetor_cores_nos.append(TONALIDADE_ROTA)
                vetor_tamanhos_nos.append(650)
            else:
                vetor_cores_nos.append(TONALIDADE_PADRAO)
                vetor_tamanhos_nos.append(450)
                
        vetor_cores_arestas = []
        vetor_larguras_arestas = []
        segmentos_rota = list(zip(rota_calculada[:-1], rota_calculada[1:]))
        
        for u, v in grafo_conexoes.edges():
            if (u, v) in segmentos_rota or (v, u) in segmentos_rota:
                vetor_cores_arestas.append(TONALIDADE_ROTA)
                vetor_larguras_arestas.append(3.5)
            else:
                vetor_cores_arestas.append(TONALIDADE_CONEXAO)
                vetor_larguras_arestas.append(1.2)
        
        nx.draw_networkx_nodes(grafo_conexoes, posicionamento, node_size=vetor_tamanhos_nos, node_color=vetor_cores_nos, edgecolors='#27ae60')
        nx.draw_networkx_edges(grafo_conexoes, posicionamento, width=vetor_larguras_arestas, edge_color=vetor_cores_arestas, alpha=0.9)
        nx.draw_networkx_labels(grafo_conexoes, posicionamento, font_size=9, font_weight='bold', font_color='#2c3e50')
        
        plt.title(f"Rota de Caminho Mínimo: {aeroporto_origem} até {aeroporto_destino}", fontsize=12, fontweight='bold', pad=15)
        plt.axis('off')
        plt.tight_layout()
        
        plt.savefig('caminho_minimo.jpeg', format='jpeg', dpi=300)
        plt.show()
        
    else:
        print("Erro: Um ou ambos os aeroportos digitados não constam na base ativa.")

if __name__ == '__main__':
    main()