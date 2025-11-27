import networkx as nx
import json
import os

class KGManager:
    def __init__(self, data_path="data/generated_data.json"):
        self.graph = nx.DiGraph()
        self.data_path = data_path
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.data_path):
            print(f"Data file not found at {self.data_path}")
            return

        with open(self.data_path, 'r') as f:
            data = json.load(f)

        # Add Users
        for user in data.get("users", []):
            self.graph.add_node(user["id"], type="User", name=user["name"], preferences=user["preferences"])

        # Add Restaurants
        for restaurant in data.get("restaurants", []):
            self.graph.add_node(restaurant["id"], type="Restaurant", name=restaurant["name"], cuisine=restaurant["cuisine"], location=restaurant["location"])

        # Add Dishes
        for dish in data.get("dishes", []):
            self.graph.add_node(dish["id"], type="Dish", name=dish["name"], price=dish["price"], attributes=dish["attributes"])
            # Link Dish to Restaurant
            self.graph.add_edge(dish["restaurant_id"], dish["id"], relation="serves")

        # Add Ingredients
        for ingredient in data.get("ingredients", []):
            self.graph.add_node(ingredient["id"], type="Ingredient", name=ingredient["name"])

        # Link Dishes to Ingredients
        for relation in data.get("dish_ingredients", []):
            dish_id = relation["dish_id"]
            for ingredient_id in relation["ingredient_ids"]:
                self.graph.add_edge(dish_id, ingredient_id, relation="contains")

        # Add Orders (History)
        for order in data.get("orders", []):
            self.graph.add_node(order["id"], type="Order", timestamp=order["timestamp"])
            self.graph.add_edge(order["user_id"], order["id"], relation="placed")
            for dish_id in order["dish_ids"]:
                self.graph.add_edge(order["id"], dish_id, relation="includes")

    def get_graph(self):
        return self.graph

    def get_node_attributes(self, node_id):
        if self.graph.has_node(node_id):
            return self.graph.nodes[node_id]
        return None

    def get_neighbors(self, node_id):
        if self.graph.has_node(node_id):
            return list(self.graph.neighbors(node_id))
        return []

if __name__ == "__main__":
    kg = KGManager()
    print(f"Graph created with {kg.graph.number_of_nodes()} nodes and {kg.graph.number_of_edges()} edges.")
    print("Nodes:", kg.graph.nodes(data=True))
