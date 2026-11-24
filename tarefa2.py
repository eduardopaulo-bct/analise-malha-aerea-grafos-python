# Grupo 14 -: Paulo Eduardo , Sophia Dumette e Eduardo Fernandez
# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx
import math

def obter_distancia_geodesica(latitude_orig, longitude_orig, latitude_dest, longitude_dest):
    raio_terra = 6371.0
    rad_lat1, rad_lat2 = math.radians(latitude_orig), math.radians(latitude_dest)
    diferenca_latitude, diferenca_longitude = math.radians(latitude_dest - latitude_orig), math.radians(longitude_dest - longitude_orig)
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
    
    mapeamento_aeroportos = aeroportos_filtrados.set_index('IATA')[['Name', 'Latitude', 'Longitude', 'City']].to_dict('index')

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

    print(">>> INDICADORES DA REDE <<<")
    graus_nos = [grau for no, grau in rede_voos.degree()]
    print(f"Grau Medio Obtido: {sum(graus_nos)/len(graus_nos):.2f}")
    print(f"Conectividade de Vertices: {nx.node_connectivity(rede_voos)}")
    print(f"Conectividade de Arestas: {nx.edge_connectivity(rede_voos)}")
    
    caminhos_curtos = dict(nx.all_pairs_dijkstra_path_length(rede_voos, weight='weight'))
    for no in rede_voos.nodes():
        excentricidade_no = max(caminhos_curtos[no].values())
        print(f"Excentricidade do No {no}: {excentricidade_no:.2f} km")
    
    diametro_final = max([max(d.values()) for d in caminhos_curtos.values()])
    print(f"Diametro Total Ponderado: {diametro_final:.2f} km")

if __name__ == '__main__':
    main()