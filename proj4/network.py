import numpy as np
import random, math, pickle, datetime
from os import system, name

data_entries = []
my_time = datetime.datetime.now()
LEARNING_RATE = .05
GLOBAL_INPUTS = 0
TIMESTAMP = (my_time.strftime("%m-%d-%Y %I.%M.%S%p"))

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
        return current_input

    #list of oututs is a 
    def back_propogate(self, list_of_outputs, target):
        # Errors of the final layer
        self.output_error_list = []
        for i, entry in enumerate(list_of_outputs):
            output_error = entry*(1-entry)*(target[i] - entry)
            self.output_error_list.append(output_error)


        #Calcute last layer errors
        l = len(self.layers)-1
        self.layers[l].errors = []
        for col in range(1, self.layers[l].num_neurons):
            sums = 0
            for row in range(self.layers[l].output_dim):
                sums += self.layers[l].weights[row][col] * self.output_error_list[row]
            error = self.layers[l].inputs[col] * (1 - self.layers[l].inputs[col]) * sums
            self.layers[l].errors.append(error)
        
        
        #Now figure out the errors for each layer
        for l in range(len(self.layers)-2, 0, -1):
            self.layers[l].errors = []
            for col in range(1, self.layers[l].num_neurons):
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
                    self.layers[l].weights[row][col] += LEARNING_RATE * self.layers[l+1].errors[row] * self.layers[l].inputs[col]

    def train(self, input_x, target):
        result = self.feed_forward(input_x)
        self.back_propogate(result, target)
        self.learn()

    def test(self, input_x):
        return self.feed_forward(input_x)        

    def save_model(self, file_path):    
        my_file = open(file_path, 'wb')
        pickle.dump(self, my_file)
        my_file.close()
            

class Layer():
    def __init__(self, output_dim, num_neurons, activation="sigmoid"):
        self.output_dim = output_dim
        self.num_neurons = num_neurons+1
        self.weights = np.zeros((output_dim, num_neurons+1), dtype=np.float128)
        self.inputs = []
        self.outputs = []
        self.errors = []
        self.activation = activation
        for i in range(len(self.weights)): #Row
            for j in range(len(self.weights[i])): #Col
                global GLOBAL_INPUTS
                self.weights[i][j] = random.uniform(-0.1, 0.1)
                #self.weights[i][j] = random.uniform(-1/math.sqrt(GLOBAL_INPUTS), 1/math.sqrt(GLOBAL_INPUTS))
                    

    def accept_input(self, input_x):
        temp = [1.0]
        temp.extend(input_x)
        input_x = temp
        self.inputs = input_x
        output = np.matmul(self.weights, input_x)
        if self.activation == "sigmoid":
            self.outputs = Layer.sigmoid(output)
        elif self.activation == "relu":
            self.outputs = Layer.relu(output)
        elif self.activation == "softmax":
            self.outputs = Layer.softmax(output)
        return self.outputs

    @staticmethod
    def sigmoid(z):
        return 1/(1 + np.exp(-z))

    @staticmethod
    def relu(z):
        for i, val in enumerate(z):
            if val < 0:
                z[i] = 0
        return z

    @staticmethod
    def softmax(z):
        bottom = 0
        temp = np.exp(z)
        for i in temp:
            bottom += i
        z = np.exp(z)/bottom
        return z


#Create the network
total_attributes = 0
listOfDicts = {}

def read_examples(file_path, delim):
    global listOfDicts
    data_list = []
    file = open(file_path)
    for line in file:
        entry = line.strip("\n").split(delim)
        data_list.append(entry)
    file.close()
    global data_entries
    data_entries = data_list

def process_test(inputs):
    result = []
    for i, data in enumerate(inputs):
        result.append(listOfDicts[i][data])
    return result

def process_numbers(example):
    result = []
    for val in example:
        result.append(int(val)/16)
    return result 


def tutorial():
    network = Network([
        Layer(output_dim=2, num_neurons=2),
        Layer(output_dim=1, num_neurons=2)
    ])
    network.layers[0].weights = np.array([[1, 1, 0.5],
                                         [1, -1, 2]])

    network.layers[1].weights = np.array([[1, 1.5, -1]])

    network.train([0, 1], [1])
    print("Hrlp")

def numbers():
    global GLOBAL_INPUTS
    print("Training Data")
    read_examples("digits-training.data", " ")
    GLOBAL_INPUTS = 64
    network = Network([ 
        Layer(output_dim=42, num_neurons=64),
        Layer(output_dim=10, num_neurons=42, activation='softmax')
    ])

    episodes = len(data_entries)
    for epoc in range(1):
        for i, example in enumerate(data_entries):
            if i == episodes:
                break
            _ = system('clear')
            print("Training Data: Epoch #", epoc, ", Example", i, "/", episodes)
            expected = np.zeros(10, dtype=np.float128)
            expected[int(example[-1])] = 1
            network.train(process_numbers(example[:-1]), expected)

    network.save_model("Handwritten Models/" + TIMESTAMP)
    
    read_examples("digits-test.data", " ")
    correct = 0
    trials = 0
    for i, example in enumerate(data_entries):
        _ = system('clear')
        print("Testing Data: Example", i, "/", len(data_entries))
        expected = np.zeros(10, dtype=np.float128)
        expected[int(example[-1])] = 1
        result = network.test(process_numbers(example[:-1]))
        if(int(example[-1]) == np.argmax(result)):
            correct += 1
        trials += 1
    print("Number Correct: ", correct)
    print("Trials: ", trials)
    print("Accuracy:", correct/trials)

def process_weather(example):
    # [0-Strong, 0-Weak, 1-Warm, 1-Moderate, 1-Weak, 2-Warm, 2-Cool, 3-Sunny, 3-Cloudy, 3-Rainy]
    translate = [
        {
            "Strong": [1, 0],
            "Weak": [0, 1]
        },
        {
            "Warm": [1, 0, 0],
            "Moderate": [0, 1, 0],
            "Cold": [0, 0, 1]
        },
        {
            "Warm": [1, 0],
            "Cool": [0, 1]
        },
        {
            "Sunny": [1, 0, 0],
            "Cloudy": [0, 1, 0],
            "Rainy": [0, 0, 1]
        }
    ]
    output = []
    output.extend(translate[0][example[0]])
    output.extend(translate[1][example[1]])
    output.extend(translate[2][example[2]])
    output.extend(translate[3][example[3]])
    return output
    

def weather():
    read_examples("fishingNN.data", ",")
    global GLOBAL_INPUTS
    GLOBAL_INPUTS = 10
    network = Network([
        Layer(output_dim=2, num_neurons=10, activation="softmax")
    ])
    for i in range(10):
        for example in data_entries:
            expected = example[-1]
            if (expected == "Yes"):
                expected = [1, 0]
            else:
                expected = [0, 1]
            network.train(process_weather(example[:-1]), expected)
    network.save_model("Weather Models/" + TIMESTAMP)
    for example in data_entries:
        expected = example[-1]
        result = network.test(process_weather(example[:-1]))
        print(result, expected)

def test_weather_model(file_name):
    my_file = open(file_name, 'rb')
    network = pickle.load(my_file)
    my_file.close()
    read_examples("fishingNN.data", ",")
    for example in data_entries:
        expected = example[-1]
        result = network.test(process_weather(example[:-1]))
        print(result, expected)

    
# test_weather_model("Weather Models/04-04-2020 03.16.50PM")
numbers()