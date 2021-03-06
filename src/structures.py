import networkx as nx


class Plant:
    def __init__(self, node, power=0.0, cost=0.0):
        self.node = node
        self.power = power
        self.cost = cost

    def __hash__(self):
        return hash((self.node, self.power))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.node == self.node and other.power == self.power


class ImmutableGraph(nx.Graph):
    def __hash__(self):
        return sum((hash(n) for n in self.nodes()))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and nx.is_isomorphic(other, self)


class Network:
    def __init__(self, graph, plant):
        self.graph = ImmutableGraph(graph)
        self.plant = plant
        self.demand = self.calculate_demand()
        self.cost = self.calculate_cost()

    def calculate_demand(self):
        return sum((data["demand"] for node, data in self.graph.nodes(data=True)))

    def calculate_cost(self):
        cost = sum((data["cost"] for n1, n2, data in self.graph.edges(data=True)))
        cost += self.plant.cost
        return cost

    def is_valid(self):
        return len(nx.connected_component_subgraphs(self.graph)) == 1 and self.plant.power >= self.demand

    def __hash__(self):
        return hash((self.graph, self.plant))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.graph == self.graph and other.plant == self.plant


class Solution:
    def __init__(self, network_list=None):
        if network_list is None:
            network_list = []
        self.network_list = network_list
        self.cost = self.calculate_cost()
        self.times_used = 0

    def calculate_cost(self):
        return sum((network.cost for network in self.network_list))

    def is_valid(self):
        return all((network.is_valid() for network in self.network_list))

    def __hash__(self):
        return sum((hash(network) for network in self.network_list))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and all(network in other.network_list for network in self.network_list)


class Config:

    defaults = {
        'change_network_chance': 0,
        'cost_of_power': lambda x: 0,
        'max_times_used': 0,
        'minimal_cost': 0,
        'number_of_max_iterations': 0,
        'number_of_neighbours': 0,
        'number_of_solutions': 0
    }

    def __init__(self, **kwargs):
        for key in Config.defaults:
            setattr(self, key, kwargs.get(key, Config.defaults[key]))
