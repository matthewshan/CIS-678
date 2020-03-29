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
        self.output_error_list = []

    def feed_forward(self, input_x):
        list_of_outputs = []
        current_input = np.array(input_x)
        # For each layer, take this input and give me the input for the next layer, until we get y
        for layer in self.layers:
            current_input = layer.accept_input(current_input)
            list_of_outputs = current_input
        return list_of_outputs

    #list of oututs is a 
    def back_propogate(self, list_of_outputs, target):
        # Errors of the final layer
        self.output_error_list = []
        for i, entry in enumerate(list_of_outputs):
            output_error = (target[i] - entry)*entry*(1-entry)
            self.output_error_list.append(output_error)
        #Calcute last layer errors
        l = len(self.layers)-1
        for row in range(self.layers[l].output_dim):
            sums = 0
            for col in range(self.layers[l].num_neurons):
                for e in self.output_error_list:
                    sums += self.layers[l].weights[row][col] * e
                error = self.layers[l].outputs[row] * (1 - self.layers[l].outputs[row]) * sums
                self.layers[l].errors.append(error)
        
        
        #Now figure out the errors for each layer
        for l in range(len(self.layers)-2, -1, -1):
            for row in range(self.layers[l].output_dim):
                sums = 0
                for col in range(self.layers[l].num_neurons):
                    for e in self.layers[l+1].errors:
                        sums += self.layers[l].weights[row][col] * e
                    error = self.layers[l].outputs[row] * (1 - self.layers[l].outputs[row]) * sums
                    self.layers[l].errors.append(error)      
    
    def learn(self):
        for l in range(len(self.layers)-1, 0, -1):
            for row in range(self.layers[l-1].output_dim):
                for col in range(self.layers[l-1].num_neurons):
                    temp1 = self.layers[l].errors[row]
                    temp2 = self.layers[l-1].outputs[row]
                    self.layers[l-1].weights[row][col] += LEARNING_RATE *  temp1 * temp2

    def train(self, input_x, target):
        result = self.feed_forward(input_x)
        self.back_propogate(result, target)
        self.learn()

    def test(self, input_x):
        return self.feed_forward(input_x)            
            

class Layer():
    def __init__(self, output_dim, num_neurons):
        self.output_dim = output_dim
        self.num_neurons = num_neurons
        self.weights = np.zeros((output_dim, num_neurons))
        self.inputs = []
        self.outputs = []
        self.errors = []
        for i in range(len(self.weights)): #Row
            for j in range(len(self.weights[i])): #Col
                if j == 0:
                    self.weights[i][j] = 1
                else:
                    self.weights[i][j] = random.uniform(-0.01, 0.01)
                    

    def accept_input(self, input_x):
        input_x = [1] + input_x
        self.inputs = input_x
        output = np.matmul(self.weights, input_x)
        self.outputs = Layer.sigmoid(output)
        return self.outputs

    @staticmethod
    def sigmoid(z):
        return 1/(1 + np.exp(-z))

#Create the network
total_attributes = 0
listOfDicts = {}

def read_examples(file_path):
    global listOfDicts
    data_list = []
    file = open(file_path)
    for line in file:
        entry = line.strip("\n").split(",")
        # by index, assign each attribute value a numerical value based on the order it was first encountered
        for index, attributeVal in enumerate(entry[:-1]):
            if (index in listOfDicts and attributeVal in listOfDicts[index]):
                # If it's already been encountered, translate the attribute to the value it received
                entry[index] = listOfDicts[index][attributeVal]
            else:
                # otherwise, register the attribute value at this index with the value one higher than the last value registered at this index
                # list of dicts = [{"hot": 0, "cold": 1, "lukewarm": 2}, {"sunny": 0, "cloudy": 1, "rainy": 2}]
                if(not index in listOfDicts):
                    listOfDicts[index] = {}
                listOfDicts[index][attributeVal] = len(listOfDicts[index].keys())
                entry[index] = listOfDicts[index][attributeVal]
        data_list.append(entry)
        global total_attributes
        total_attributes = len(entry) - 1
    file.close()
    global data_entries
    data_entries = data_list

def process_test(inputs):
    result = []
    for i, data in enumerate(inputs):
        result.append(listOfDicts[i][data])
    return result

def test():
    read_examples("test.data")
    network = Network([
        Layer(output_dim=2, num_neurons=2),
        Layer(output_dim=1, num_neurons=2)
    ])
    for example in data_entries:
        network.train(example[:-1], [1])


def weather():
    read_examples("fishingNN.data")
    network = Network([
    Layer(output_dim=2, num_neurons=4),
    Layer(output_dim=1, num_neurons=2)
])
    for _ in range(1):
        for example in data_entries:
            expected = example[-1]
            if (expected == "Yes"):
                expected = [1]
            else:
                #print(expected)
                expected = [0]
            network.train(example[:-1], expected)

    test_data = process_test(["Weak", "Cold", "Cool", "Rainy"])
    print(network.test(test_data))

    test_data = process_test(["Strong", "Warm", "Warm", "Rainy"])
    print(network.test(test_data))

    test_data = process_test(["Weak", "Cold", "Cool", "Rainy"])
    print(network.test(test_data))
    

weather()