import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#fuzzy input variables
traffic = ctrl.Antecedent(np.arange(0, 11, 1), 'traffic')
weather = ctrl.Antecedent(np.arange(0, 11, 1), 'weather')
road = ctrl.Antecedent(np.arange(0, 11, 1), 'road') 
time_of_day = ctrl.Antecedent(np.arange(0, 11, 1), 'time_of_day')  # 0 = Early, 5 = Midday, 10 = Evening
road_type = ctrl.Antecedent(np.arange(0, 3, 1), 'road_type')       # 0 = Street, 1 = Main Road, 2 = Highway

#fuzzy output variable
cost = ctrl.Consequent(np.arange(0, 51, 1), 'cost')

#fuzzy sets
traffic.automf(3)
weather.automf(3)
road.automf(3)

#Custom fuzzy sets
time_of_day['early'] = fuzz.trimf(time_of_day.universe, [0, 0, 5])
time_of_day['midday'] = fuzz.trimf(time_of_day.universe, [3, 5, 7])
time_of_day['evening'] = fuzz.trimf(time_of_day.universe, [5, 10, 10])

road_type['street'] = fuzz.trimf(road_type.universe, [0, 0, 1])
road_type['main'] = fuzz.trimf(road_type.universe, [0, 1, 2])
road_type['highway'] = fuzz.trimf(road_type.universe, [1, 2, 2])

cost['low'] = fuzz.trimf(cost.universe, [0, 10, 20])
cost['medium'] = fuzz.trimf(cost.universe, [15, 25, 35])
cost['high'] = fuzz.trimf(cost.universe, [30, 40, 50])

#Fuzzy Rules
rules = [
    ctrl.Rule(traffic['poor'] | weather['poor'], cost['high']),
    ctrl.Rule(road['poor'] & road_type['street'], cost['high']),
    ctrl.Rule(time_of_day['evening'] & traffic['average'], cost['medium']),
    ctrl.Rule(weather['average'] & traffic['average'], cost['medium']),
    ctrl.Rule(road['good'] & road_type['main'], cost['low']),
    ctrl.Rule(time_of_day['early'] & road_type['highway'] & traffic['good'], cost['low']),
    ctrl.Rule(weather['good'] & road['good'] & road_type['highway'], cost['low']),
    ctrl.Rule(road['average'] & weather['average'] & time_of_day['midday'], cost['medium']),
]

cost_ctrl = ctrl.ControlSystem(rules)
cost_sim = ctrl.ControlSystemSimulation(cost_ctrl)

def heuristic(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def a_star(graph, start, goal, traffic_val, weather_val, road_val, time_val, road_type_val):
    try:
        cost_sim.input['traffic'] = traffic_val
        cost_sim.input['weather'] = weather_val
        cost_sim.input['road'] = road_val
        cost_sim.input['time_of_day'] = time_val
        cost_sim.input['road_type'] = road_type_val
        cost_sim.compute()
        fuzzy_cost = cost_sim.output['cost']
    except Exception as e:
        raise ValueError(f"Fuzzy cost calculation failed: {e}")

    path = nx.astar_path(graph, start, goal, heuristic=lambda a, b: heuristic(graph.nodes[a]['pos'], graph.nodes[b]['pos']),
                         weight=lambda u, v, d: d['weight'] + fuzzy_cost)
    return path, nx.path_weight(graph, path, weight='weight') + fuzzy_cost

def create_graph():
    G = nx.Graph()
    G.add_node('A', pos=(0, 0))
    G.add_node('B', pos=(1, 2))
    G.add_node('C', pos=(2, 0))
    G.add_node('D', pos=(3, 2))
    G.add_node('E', pos=(4, 0))

    G.add_edge('A', 'B', weight=3)
    G.add_edge('A', 'C', weight=5)
    G.add_edge('B', 'D', weight=2)
    G.add_edge('C', 'D', weight=4)
    G.add_edge('D', 'E', weight=6)

    return G

def draw_graph(graph, path=None):
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=3)

    plt.show()

if __name__ == "__main__":
    G = create_graph()
    source, destination = 'A', 'E'
    traffic_val, weather_val, road_val = 7, 6, 3
    time_val = 8
    road_type_val = 0

    path, total_cost = a_star(G, source, destination, traffic_val, weather_val, road_val, time_val, road_type_val)
    print("Optimal Path:", path)
    print("Estimated Cost with Fuzzy Logic:", total_cost)
    draw_graph(G, path)
