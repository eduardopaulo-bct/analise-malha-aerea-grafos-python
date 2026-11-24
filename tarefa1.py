# Grupo 14 -: Paulo Eduardo , Sophia Dumette e Eduardo Fernandez
# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import math

def obter_distancia_geodesica(latitude_orig, longitude_orig, latitude_dest, longitude_dest):
    raio_terra = 6371.0
    rad_lat1, rad_lat2 = math.radians(latitude_orig), math.radians(latitude_dest)
    diferenca_latitude = math.radians(latitude_dest - latitude_orig)
    diferenca_longitude = math.radians(longitude_dest - longitude_orig)
    calculo_arco = math.sin(diferenca_latitude / 2.0)**2 + math.cos(rad_lat1) * math.cos(rad_lat2) * math.sin(diferenca_longitude / 2.0)**2
    return raio_terra * (2 * math.atan2(math.sqrt(calculo_arco), math.sqrt(1 - calculo_arco)))

def main():
    tabela_aeroportos = pd.read_csv('airports.dat', header=None, 
                                    names=['ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 
                                           'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz', 'Type', 'Source'])
    tabela_rotas = pd.read_csv('routes.dat', header=None,
                               names=['Airline', 'Airline_ID', 'Source_Airport', 'Source_Airport_ID', 
                                      'Dest_Airport', 'Dest_Airport_ID', 'Codeshare', 'Stops', 'Equipment'])

    conexoes_mandarin = tabela_rotas[tabela_rotas['Airline'] == 'AE'].copy()
    
    aeroportos_filtrados = tabela_aeroportos[
        tabela_aeroportos['IATA'].notna() & 
        (tabela_aeroportos['IATA'] != '\\N') & 
        (tabela_aeroportos['IATA'] != '')
    ].drop_duplicates(subset=['IATA'])
    
    mapeamento_aeroportos = aeroportos_filtrados.set_index('IATA')[['Name', 'Latitude', 'Longitude', 'City', 'Country']].to_dict('index')

    rede_voos = nx.Graph()
    for _, linha in conexoes_mandarin.iterrows():
        origem_voo, destino_voo = linha['Source_Airport'], linha['Dest_Airport']
        if origem_voo in mapeamento_aeroportos and destino_voo in mapeamento_aeroportos:
            if origem_voo == destino_voo: continue
            lat_a, lon_a = mapeamento_aeroportos[origem_voo]['Latitude'], mapeamento_aeroportos[origem_voo]['Longitude']
            lat_b, lon_b = mapeamento_aeroportos[destino_voo]['Latitude'], mapeamento_aeroportos[destino_voo]['Longitude']
            distancia_calculada = obter_distancia_geodesica(lat_a, lon_a, lat_b, lon_b)
            if not rede_voos.has_edge(origem_voo, destino_voo):
                rede_voos.add_edge(origem_voo, destino_voo, weight=distancia_calculada)

    plt.figure(figsize=(9, 9))
    
    layout_nos = nx.spring_layout(rede_voos, seed=10, k=1.5)
    
    nx.draw_networkx_nodes(rede_voos, layout_nos, node_size=500, node_color='#2ecc71', edgecolors='#27ae60')
    nx.draw_networkx_edges(rede_voos, layout_nos, width=2.5, edge_color='#95a5a6', alpha=0.9)
    nx.draw_networkx_labels(rede_voos, layout_nos, font_size=9, font_weight='bold', font_color='#2c3e50')
    
    rotulos_distancias = nx.get_edge_attributes(rede_voos, 'weight')
    rotulos_formatados = {par: f"{valor:.0f}km" for par, valor in rotulos_distancias.items()}
    nx.draw_networkx_edge_labels(rede_voos, layout_nos, edge_labels=rotulos_formatados, font_size=8, font_color='#7f8c8d')

    plt.title("Malha Aerea Operacional - Mandarin Airlines", fontsize=11, fontweight='bold', pad=15)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('visualizacao.jpeg', format='jpeg', dpi=300)
    print("Sucesso: 'visualizacao.jpeg' gerada com novo layout!")

if __name__ == '__main__':
    main()