import matplotlib.pyplot as plt
import networkx as nx

class SemanticNetwork:
    def __init__(self):
        self.network = []

    def add_fact(self, subject, relation, obj):
        # Adding the relation (subject, relation, object) as a tuple to the network
        self.network.append((subject, relation, obj))

    def display_network(self):
        # Displaying all the facts in the network
        if not self.network:
            print("No facts in the network.")
        else:
            print("\nCurrent Semantic Network:")
            for fact in self.network:
                print(f"{fact[0]} {fact[1]} {fact[2]}")
           
            # Now let's generate and display the graph of the relationships
            self.display_graph()

    def display_graph(self):
        # Create a directed graph
        G = nx.DiGraph()
       
        # Add nodes and edges to the graph based on the facts
        for fact in self.network:
            subject, relation, obj = fact
            # Create edges like: subject -> relation -> object
            G.add_edge(subject, relation)
            G.add_edge(relation, obj)
       
        # Draw the graph using matplotlib
        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(G)  # Positioning the nodes in the graph
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
        plt.title("Semantic Network Graph")
        plt.show()

def main():
    semantic_network = SemanticNetwork()
   
    while True:
        print("\nMenu:")
        print("1. Add a new fact")
        print("2. Display all facts and graph")
        print("3. Exit")
       
        choice = input("Enter your choice (1-3): ")
       
        if choice == '1':
            # Input the number of facts
            try:
                num_facts = int(input("How many facts do you want to enter? "))
            except ValueError:
                print("Please enter a valid number.")
                continue
           
            for i in range(num_facts):
                print(f"\nFact {i + 1}:")
               
                # Input Subject, Relation, Object
                subject = input("Enter subject: ")
                relation = input("Enter relation: ")
                obj = input("Enter object: ")
               
                # Add the fact to the semantic network
                semantic_network.add_fact(subject, relation, obj)
       
        elif choice == '2':
            # Display all facts and the network graph
            semantic_network.display_network()
       
        elif choice == '3':
            # Exit the program
            print("Exiting the program.")
            break
       
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
