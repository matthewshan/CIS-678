import numpy as np
import random

data_entries = []
LEARNING_RATE = 0.01

def read_examples(file_path):
    data_list = []
    file = open(file_path)
    for line in file:
        entry = line.strip("\n").split(",")
        data_list.append(entry)
    file.close()
    return data_list

class Network():
    def __init__(self, layers):
        # List of Layer Object
        self.layers = layers
        self.output_dim = self.layers[-1].output_dim

    def feed_forward(self, input_x):
        list_of_outputs = []
        current_input = np.array(input_x)
        # For each layer, take this input and give me the input for the next layer, until we get y
        for layer in layers:
            current_input = layer.accept_input(current_input)
            list_of_outputs.append(current_input)
        return list_of_outputs

    #list of oututs is a 
    def back_propogate(self, list_of_outputs, target):
        layer_index = len(self.layers) - 1

        # Errors of the final layer
        output_error_list = []
        final_vector = list_of_outputs[-1]
        for entry in final_vector:
            output_error = (target - entry)*entry*(1-entry)
            output_error_list.append(output_error)
        self.layers[layer_index].errors = output_error_list
        
        #Now figure out the errors for each layer
        for layer in range(len(self.layesr)-2, 0, -1 ):
            

        
    #     self.back_propogate_hidden(list_of_outputs[0:-1], list_of_errors, layer_index)


    # def back_propogate_hidden(self, list_of_outputs, list_of_errors, layer_index):
    #     temp = 0
    #     layer = self.layers[layer_index]
    #     next_errors = [] 
    #     for i in layer.num_neurons:
            
    #         for k, error in enumerate(output_error_list):
                

    
    #     # layer_index = len(self.layers) - 1
    #     # current_layer = self.layers[layer_index]
    #     # # list_of_outputs[layer_index][i] == h sub i
       
    
    def learn(self, error_list):
        for layer in layers:
            for weight in layer.weights:
                error_to_use = 
                weight = weight + LEARNING_RATE*error_to_use*value_of_
            

class Layer():
    def __init__(self, output_dim, num_neurons):
        self.output_dim = output_dim
        self.num_neurons = num_neurons
        self.weights = np.zeros((output_dim, num_neurons))
        self.errors = []
        for i in self.weights: #Row
            for j in self.weights[i]: #Col
                if j == 0:
                    self.weights[i][j] = 1
                else:
                    self.weights[i][j] = random.uniform(-0.01, 0.01)
                    

    def accept_input(self, input_x):
        input_x = [1] + input_x
        output = np.matmul(self.weights, input_x)
        return Layer.sigmoid(output)

    @staticmethod
    def sigmoid(z):
        return 1/(1 + np.exp(-z))

#Create the network
network = Network([
    Layer(output_dim=2, num_neurons=4),
    Layer(output_dim=1, num_neurons=2)
])
data_entries = read_examples("fishingNN.data")