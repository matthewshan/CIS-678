import numpy as np
import random
from os import system, name

data_entries = []
LEARNING_RATE = .5

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
        current_input = np.array(input_x, dtype=np.float128)
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
        for col in range(self.layers[l].num_neurons):
            sums = 0
            for row in range(self.layers[l].output_dim):
                sums += self.layers[l].weights[row][col] * self.output_error_list[row]
            error = self.layers[l].inputs[col] * (1 - self.layers[l].inputs[col]) * sums
            self.layers[l].errors.append(error)
        
        
        #Now figure out the errors for each layer
        for l in range(len(self.layers)-2, -1 , -1):
            for col in range(self.layers[l].num_neurons):
                sums = 0
                for row in range(self.layers[l].output_dim):
                    sums += self.layers[l].weights[row][col] * self.layers[l+1].errors[row]
                error = self.layers[l].inputs[col] * (1 - self.layers[l].inputs[col]) * sums
                self.layers[l].errors.append(error)

    
    def learn(self):
        l = len(self.layers)-1
        for row in range(self.layers[l].output_dim):
            for col in range(self.layers[l].num_neurons):
                self.layers[l].weights[row][col] += LEARNING_RATE *  self.output_error_list[row] * self.layers[l].inputs[col]

        for l in range(len(self.layers)-2, -1, -1):
            for row in range(self.layers[l].output_dim):
                for col in range(self.layers[l].num_neurons):
                    self.layers[l].weights[row][col] += LEARNING_RATE *  self.layers[l+1].errors[row] * self.layers[l].inputs[col]

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
        self.weights = np.zeros((output_dim, num_neurons), dtype=np.float128)
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

def read_examples(file_path, delim):
    global listOfDicts
    data_list = []
    file = open(file_path)
    for line in file:
        entry = line.strip("\n").split(delim)
        # # by index, assign each attribute value a numerical value based on the order it was first encountered
        # for index, attributeVal in enumerate(entry[:-1]):
        #     if (index in listOfDicts and attributeVal in listOfDicts[index]):
        #         # If it's already been encountered, translate the attribute to the value it received
        #         entry[index] = listOfDicts[index][attributeVal]
        #     else:
        #         # otherwise, register the attribute value at this index with the value one higher than the last value registered at this index
        #         # list of dicts = [{"hot": 0, "cold": 1, "lukewarm": 2}, {"sunny": 0, "cloudy": 1, "rainy": 2}]
        #         if(not index in listOfDicts):
        #             listOfDicts[index] = {}
        #         listOfDicts[index][attributeVal] = len(listOfDicts[index].keys())
        #         entry[index] = listOfDicts[index][attributeVal]
        data_list.append(entry)
        # global total_attributes
        # total_attributes = len(entry) - 1
    file.close()
    global data_entries
    data_entries = data_list

def process_test(inputs):
    result = []
    for i, data in enumerate(inputs):
        result.append(listOfDicts[i][data])
    return result

def test():
    read_examples("test.data", ",")
    network = Network([
        Layer(output_dim=4, num_neurons=2),
        Layer(output_dim=2, num_neurons=2),
        Layer(output_dim=1, num_neurons=2)
    ])
    for example in data_entries:
        network.train(example[:-1], [1])


def numbers():
    print("Training Data")
    read_examples("digits-training.data", " ")
    network = Network([
        Layer(output_dim=32, num_neurons=64),
        Layer(output_dim=16, num_neurons=32),
        Layer(output_dim=10, num_neurons=16)
    ])

    episodes = 500
    for i, example in enumerate(data_entries):
        if i == 500:
            break
        _ = system('clear')
        print("Training Data: Example", i, "/", episodes)
        expected = np.zeros(10, dtype=np.float128)
        expected[int(example[-1])] = 1
        network.train(example[:-1], expected)
    
    read_examples("digits-test.data", " ")
    correct = 0
    trials = 0
    for i, example in enumerate(data_entries):
        
        _ = system('clear')
        print("Testing Data: Example", i, "/", len(data_entries))
        expected = np.zeros(10, dtype=np.float128)
        expected[int(example[-1])] = 1
        result = network.test(example[:-1])
        if(int(example[-1]) == np.argmax(result)):
            correct += 1
        trials += 1
    print("Number Correct: ", correct)
    print("Trials: ", trials)
    print("Accuracy:", correct/trials)



def weather():
    read_examples("fishing.data", ",")
    network = Network([
        Layer(output_dim=8, num_neurons=4),
        Layer(output_dim=4, num_neurons=8),
        Layer(output_dim=2, num_neurons=4)
    ])
    for _ in range(1):
        for example in data_entries:
            expected = example[-1]
            if (expected == "Yes"):
                expected = [1, 0]
            else:
                #print(expected)
                expected = [0, 1]
            network.train(example[:-1], expected)

    # test_data = process_test(["Weak", "Cold", "Cool", "Rainy"])
    test_data = [0, -1, 0, -1]
    print(network.test(test_data))

    # test_data = process_test(["Strong", "Warm", "Warm", "Rainy"])
    test_data = [1, 1, 1, -1]
    print(network.test(test_data))

    #test_data = process_test(["Weak", "Cold", "Cool", "Rainy"])
    test_data = [0, -1, 0, -1]
    print(network.test(test_data))
    
weather()