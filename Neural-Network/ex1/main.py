import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class Neuron:  
    def __init__(self, n_inputs, bias = 0., weights = None):  
        self.b = bias
        if weights: self.ws = np.array(weights)
        else: self.ws = np.random.rand(n_inputs)

    def _f(self, x): #activation function (here: leaky_relu)
        return max(x*.1, x)   

    def __call__(self, xs): #calculate the neuron's output: multiply the inputs with the weights and sum the values together, add the bias value,
                            # then transform the value via an activation function
        return self._f(xs @ self.ws + self.b) 
    
    def sig(x):
        return 1/(1 + np.exp(-x))
   
    def train(self, training_data, learning_rate=0.1, epochs=100):
        for _ in range(epochs):
            for inputs, target_output in training_data:
                # Forward propagation
                output = self.__call__(inputs)

                # Backpropagation
                error = target_output - output
                delta_weights = learning_rate * error * inputs
                delta_bias = learning_rate * error

                # Update weights and bias
                self.ws += delta_weights
                self.b += delta_bias
                
class NeuralNetwork:
    def __init__(self):
        
        self.input_layer = [Neuron(3) for _ in range(3)]
        self.hidden_layer1 = [Neuron(3) for _ in range(4)]
        self.hidden_layer2 = [Neuron(4) for _ in range(4)]
        self.output_layer = Neuron(4)

    def __call__(self, xs):
        
        hidden_layer1_outputs = [neuron(xs) for neuron in self.hidden_layer1]
        hidden_layer2_outputs = [neuron(hidden_layer1_outputs) for neuron in self.hidden_layer2]
        output = self.output_layer(hidden_layer2_outputs)
        return output

    def train(self, training_data, learning_rate=0.1, epochs=100):
        for _ in range(epochs):
            for inputs, target_output in training_data:
                
                hidden_layer1_outputs = [neuron(inputs) for neuron in self.hidden_layer1]
                hidden_layer2_outputs = [neuron(hidden_layer1_outputs) for neuron in self.hidden_layer2]
                output = self.output_layer(hidden_layer2_outputs)

                
                error = target_output - output
                delta_weights_output = learning_rate * error * np.array(hidden_layer2_outputs)
                delta_bias_output = learning_rate * error

                delta_weights_hidden2 = [
                    learning_rate * delta_w * np.array(hidden_layer1_outputs)
                    for delta_w in self.output_layer.ws
                ]
                delta_bias_hidden2 = [learning_rate * delta_w for delta_w in self.output_layer.ws]

                delta_weights_hidden1 = [
                    learning_rate * delta_w * np.array(inputs)
                    for delta_w in np.concatenate([neuron.ws for neuron in self.hidden_layer2])
                ]
                delta_bias_hidden1 = [learning_rate * delta_w for delta_w in np.concatenate([neuron.ws for neuron in self.hidden_layer2])]

                
                self.output_layer.ws += delta_weights_output
                self.output_layer.b += delta_bias_output

                for neuron, delta_w, delta_b in zip(self.hidden_layer2, delta_weights_hidden2, delta_bias_hidden2):
                    neuron.ws += delta_w
                    neuron.b += delta_b

                for neuron, delta_w, delta_b in zip(self.hidden_layer1, delta_weights_hidden1, delta_bias_hidden1):
                    neuron.ws += delta_w
                    neuron.b += delta_b

    def visualize(self):
        G = nx.DiGraph()

        
        G.add_nodes_from(["IL {}".format(i+1) for i in range(3)])
        G.add_nodes_from(["HL 1 {}".format(i+1) for i in range(4)])
        G.add_nodes_from(["HL 2 {}".format(i+1) for i in range(4)])
        G.add_node("OL")

        
        for i in range(3):
            for j in range(4):
                G.add_edge("IL {}".format(i+1), "HL 1 {}".format(j+1))
        for i in range(4):
            for j in range(4):
                G.add_edge("HL 1 {}".format(i+1), "HL 2 {}".format(j+1))
        for i in range(4):
            G.add_edge("HL 2 {}".format(i+1), "OL")

        
        pos = {}
        for i in range(3):
            pos["IL {}".format(i+1)] = (0, i)
        for i in range(4):
            pos["HL 1 {}".format(i+1)] = (1, i)
        for i in range(4):
            pos["HL 2 {}".format(i+1)] = (2, i)
        pos["OL"] = (3, 1)

        
        nx.draw(G, pos=pos, with_labels=True, node_size=1000, node_color='gray', font_size=10, font_color='black', font_weight='bold', arrowsize=15, arrowstyle='->', edge_color='gray')

        plt.show()

network = NeuralNetwork()
network.visualize()