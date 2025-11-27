import networkx as nx

class Explainer:
    def __init__(self, kg_manager):
        self.kg_manager = kg_manager
        self.graph = kg_manager.get_graph()

    def find_paths(self, start_node, end_node, max_depth=3):
        """
        Find simple paths between two nodes in the KG.
        """
        try:
            paths = list(nx.all_simple_paths(self.graph, source=start_node, target=end_node, cutoff=max_depth))
            return paths
        except nx.NetworkXNoPath:
            return []
        except nx.NodeNotFound:
            return []

    def translate_path_to_nl(self, path):
        """
        Translate a path (list of node IDs) into a natural language sentence.
        """
        if not path or len(path) < 2:
            return ""

        explanation_parts = []
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            u_data = self.graph.nodes[u]
            v_data = self.graph.nodes[v]
            edge_data = self.graph.get_edge_data(u, v)
            relation = edge_data.get("relation", "related to")
            
            # Simple template: "A [relation] B"
            part = f"{u_data.get('name', u)} {relation} {v_data.get('name', v)}"
            explanation_parts.append(part)

        return " which ".join(explanation_parts)

    def explain_recommendation(self, user_id, dish_id):
        """
        Generate an explanation for why a dish is recommended to a user.
        """
        # Heuristic: Find paths from User -> Order -> Dish (history) or User -> Preference -> Dish (if we had preference nodes)
        # For this simple graph, we look for:
        # 1. User -> Order -> Dish (Re-ordering)
        # 2. User -> Order -> Dish (similar attributes? - requires more complex graph)
        
        # Let's try to find paths from User to Dish directly or via history
        # Since our graph is directed User -> Order -> Dish, we can find if they ordered it before.
        
        paths = self.find_paths(user_id, dish_id, max_depth=3)
        
        if paths:
            reasons = [self.translate_path_to_nl(p) for p in paths]
            return f"Recommended because: {'; '.join(reasons)}"
        
        # If no direct path, maybe check if they ordered something from the same restaurant?
        # User -> Order -> Dish <-(serves)- Restaurant -(serves)-> TargetDish
        # This requires undirected traversal or specific queries.
        
        # Let's try an undirected view for broader context
        undirected_graph = self.graph.to_undirected()
        try:
            paths = list(nx.all_simple_paths(undirected_graph, source=user_id, target=dish_id, cutoff=3))
            if paths:
                # Filter for meaningful paths, e.g., User - Order - Dish - Ingredient - Dish
                # For now, just take the first one
                return f"Recommended because it is related to your history: {self.translate_path_to_nl(paths[0])}"
        except:
            pass
            
        return "Recommended based on general popularity."

if __name__ == "__main__":
    from src.core.kg_manager import KGManager
    kg = KGManager()
    explainer = Explainer(kg)
    
    # Test explanation
    if len(kg.graph.nodes) > 0:
        # Get a random user and dish
        users = [n for n, d in kg.graph.nodes(data=True) if d.get('type') == 'User']
        dishes = [n for n, d in kg.graph.nodes(data=True) if d.get('type') == 'Dish']
        
        if users and dishes:
            u = users[0]
            d = dishes[0]
            print(f"Explaining recommendation for User {u} and Dish {d}")
            print(explainer.explain_recommendation(u, d))
