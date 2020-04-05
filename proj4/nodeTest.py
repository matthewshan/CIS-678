import random, math
import numpy as np

data_entries = []
# The learning rate for the learn method
LEARNING_RATE = 0.1
WEATHER_FLAG = True

class Node:
    def __init__(self):
        # The actual value of the node
        self.value = 0
        # The calculated error for this node
        self.error = 0
        # All the children of this node
        # Should be something like follows:
        # Children = [[child1, 1], [child2, 2.5], [child3, 0.85], [child4, 1.2]]
        # children[0][1] would return whatever weight is associated with the first child
        self.children = []
        # All the parents of this node (found out from the parents), should be similar to children
        self.parents = []
        # Whether this is an output node or not
        self.isTop = False
        # Whether this is a bias node or not
        self.isBias = False
        self.greetedKids = False

    @staticmethod
    def sigmoid(z):
        return 1/(1 + math.exp(-z))

    @staticmethod
    def softmax(z):
        bottom = 0
        temp = np.exp(z)
        for i in temp:
            bottom += i
        z = np.exp(z)/bottom
        return z

    @staticmethod
    def relu(z):
        for i, val in enumerate(z):
            if val < 0:
                z[i] = 0
        return z

    # This method needs only to be called on the top nodes. It will update their value, as well as the children's values accordingly.
    def updateNodeVal(self):
        # If there are no children (a leaf node), it will simply return the value of that node. Ie. the "termination" case
        for child in self.children:
            # child.getValue() is getting the weight to this node associated with the child
            self.value += child[0].updateNodeVal() * child[1]
        if len(self.children) != 0:
            self.value = Node.sigmoid(self.value)
        return self.value

    def getLeafs(self):
        leafList = []
        if (len(self.children) == 0):
            return self
        for child in self.children:
            leafList.append(child[0].getLeafs())
        return leafList

    # This will get the error for this single node depending on what type of node it is. 
    # The top nodes must be calculated first, thus why it only calculates one node's error. (manually have it do all output, then hidden)
    # Thus, since it only calculates one, this method must be called on the whole network eventually.
    def backProp(self, target=1):
        if self.isTop:
            self.error = (target-self.value) * self.value * (1 - self.value)
        # If it isn't a top node, be it a leaf or a hidden node
        else:
            sum = 0
            # We need to sum all the parent's error values (thus why the top nodes must be processed first), 
            # as well as the value of the weight between this node and the parent node. 
            for parent in self.parents:
                sum += parent[1] * parent[0].error
            self.error = sum * self.value * (1 - self.value)
            for child in self.children:
                child[0].backProp()
    
    # This is the last method that gets called. You only need to call it on the top nodes, 
    # and it will recursively update anything that points to it, or to any of it's children
    def learn(self):
        global LEARNING_RATE
        # If no children, nothing to update, so it will self terminate
        for child in self.children:
            # Set the weight between this node and its child to the given equation value
            child[1] = child[1] + LEARNING_RATE * child[0].error * child[0].value
            child[0].learn()

    # Add a node to the children list
    def adoptChild(self, node, weight):
        self.children.append([node, weight])

    # Let every child know this node is it's parent
    def sayHiToTheKids(self):
        if (not self.greetedKids):
            for child in self.children:
                # Let the child know their parent, and the weight between them
                child[0].sayHiToDad(self, child[1])
                child[0].sayHiToTheKids()
        self.greetedKids = True
        
    # Learn a node is a parent, as well as the weight to them
    def sayHiToDad(self, parentNode, weight):
        self.parents.append([parentNode, weight])

class NeuralNet():
    def __init__(self, rows_sizes):
        self.topNodes = []
        self.leafNodes = []

        output_nuerons = rows_sizes[0] # TOP ROW of our network
        TOTAL_ROWS = len(rows_sizes) - 1 # HEIGHT of our network
        # Does not include bias
        ROW_SIZE = rows_sizes # WIDTH of a row

        for _ in range(output_nuerons):
            # TOPNODE should be true
            newNode = Node()
            newNode.isTop = True
            self.topNodes.append(newNode)

        lastLayer = self.topNodes

        rows_sizes = rows_sizes[1:]        
        for num, rowSize in enumerate(rows_sizes):
            nextRow = []
            lastRow = (num == TOTAL_ROWS - 1)

            # Generate the bias node
            biasNode = Node()
            biasNode.value = 1
            biasNode.isBias = True
            nextRow.append(biasNode)

            # Generate the neurons of the row
            for _ in range(rowSize):
                newNode = Node()
                if (lastRow):
                    self.leafNodes.append(newNode)
                nextRow.append(newNode)

            # Connect each new node to the layer above it
            for node in lastLayer:
                if (not node.isBias):
                    for cNode in nextRow:
                        randomWeight = random.uniform(-0.01, 0.01)
                        #randomWeight = 1
                        node.adoptChild(cNode, randomWeight)
            lastLayer = nextRow

        for node in self.topNodes:
            node.sayHiToTheKids()

    def train(self, inputs, expected):
        if (len(inputs) != len(self.leafNodes)):
            raise ValueError
        # Set the leaf nodes to the appropriate values
        for i in range(1, len(self.leafNodes) + 1):
            self.leafNodes[i-1].value = inputs[i-1]

        # Calculate the new values for the output nodes
        for i, topNode in enumerate(self.topNodes):
            topNode.updateNodeVal()
        
        # Softmax those output values to get the probabilities
        topnodeValList = []
        for topNode in self.topNodes:
            topnodeValList.append(topNode.value)

        newTopnodeValues = Node.softmax(topnodeValList)
        print (newTopnodeValues)
        index = 0
        # Assign softmax'd values to the output nodes
        for topNode in self.topNodes:
            topNode.value = newTopnodeValues[index]
            index += 1

        for i, topNode in enumerate(self.topNodes):
            topNode.backProp(expected[i])
        
        for topNode in self.topNodes:
            for child in topNode.children:
                child[0].backProp()
            topNode.learn()

    def test(self, inputs):
        if (len(inputs) != len(self.leafNodes)):
            raise ValueError
        
        for i in range(1, len(self.leafNodes) + 1):
            self.leafNodes[i-1].value = inputs[i-1]

        for topNode in self.topNodes:
            topNode.updateNodeVal()

        # Softmax those output values to get the probabilities
        topnodeValList = []
        for topNode in self.topNodes:
            topnodeValList.append(topNode.value)

        newTopnodeValues = Node.softmax(topnodeValList)
        #print (newTopnodeValues)
        index = 0
        # Assign softmax'd values to the output nodes
        for topNode in self.topNodes:
            topNode.value = newTopnodeValues[index]
            index += 1

        return [endNodes.value for endNodes in self.topNodes]

#total_attributes = 0
#listOfDicts = {}

def read_examples(file_path, dl):
    #global listOfDicts
    data_list = []
    file = open(file_path)
    for line in file:
        entry = line.strip("\n").split(dl)
        # Translate the entry into numerical data
        global WEATHER_FLAG
        if (WEATHER_FLAG):
            entry = process_weather(entry)
        else:
            entry = process_numbers(entry)
        # by index, assign each attribute value a numerical value based on the order it was first encountered
        #for index, attributeVal in enumerate(entry[:-1]):
            #if (index in listOfDicts and attributeVal in listOfDicts[index]):
            #    # If it's already been encountered, translate the attribute to the value it received
            #    entry[index] = listOfDicts[index][attributeVal]
            #else:
            #    # otherwise, register the attribute value at this index with the value one higher than the last value registered at this index
            #    # list of dicts = [{"hot": 0, "cold": 1, "lukewarm": 2}, {"sunny": 0, "cloudy": 1, "rainy": 2}]
            #    if(not index in listOfDicts):
            #        listOfDicts[index] = {}
            #    listOfDicts[index][attributeVal] = len(listOfDicts[index].keys())
            #    entry[index] = listOfDicts[index][attributeVal]
        data_list.append(entry)
        #global total_attributes
        #total_attributes = len(entry) - 1
    file.close()
    global data_entries
    data_entries = data_list

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
    #print(str(example))
    #print(type(example))
    output = []
    output.extend(translate[0][example[0]])
    output.extend(translate[1][example[1]])
    output.extend(translate[2][example[2]])
    output.extend(translate[3][example[3]])
    if (len(example) > 4):
        output.append(example[4])
    return output

def process_numbers(example):
    result = []
    for val in example:
        result.append(int(val)/16)
    return result 

# def process_test(inputs):
#     result = []
#     for i, data in enumerate(inputs):
#         result.append(listOfDicts[i][data])
#     return result

def tryNetwork():
    network = NeuralNet([1,2,2])
    data_entry = [0.5, 3]
    network.train(data_entry, [1])

def weather():
    read_examples("fishingNN.data", ",")
    network = NeuralNet([2, 8, 10])
    for _ in range(10):
        for example in data_entries:
            #print(example)
            expected = example[-1]
            if (expected == "Yes"):
                expected = [1, 0]
            else:
                #print(expected)
                expected = [0, 1]
            network.train(example[:-1], expected)
        #print("Finished Epoch")

    # test_data = process_weather(["Weak", "Cold", "Cool", "Rainy"])
    # print(network.test(test_data))

    # test_data = process_weather(["Strong", "Warm", "Warm", "Rainy"])
    # print(network.test(test_data))

    # test_data = process_weather(["Weak", "Cold", "Cool", "Sunny"])
    # print(network.test(test_data))

    for example in data_entries:
        expected = example[-1]
        result = network.test(example[:-1])
        print(result, expected)

def makeArray(index):
    array = [10]
    for ind in range(9):
        if (ind == index):
            array.append(1)
        else:
            array.append(0)
    return array

def numbers():
    read_examples("digits-training.data", " ")
    print("Finished reading examples")
    network = NeuralNet([10, 42, 64])
    print("Made Neural Net")
    for _ in range(10):
        for example in data_entries:
            expected = example[-1]
            expected = makeArray(expected)
            network.train(example[:-1], expected)
            print("Finished Training")

    test_data = [0, 0, 8, 15, 16, 13, 0, 0, 0, 1, 11, 9, 11, 16, 1, 0, 0, 0, 0, 0, 7, 14, 0, 0, 0, 0, 3, 4, 14, 12, 2, 0, 0, 1, 16, 16, 16, 16, 10, 0, 0, 2, 12, 16, 10, 0, 0, 0, 0, 0, 2, 16, 4, 0, 0, 0, 0, 0, 9, 14, 0, 0, 0, 0, 7]
    print(network.test(test_data))

    for entry in data_entries[-1:-100]:
        print(network.test(entry))

#tryNetwork()
if (WEATHER_FLAG):
    weather()
else:
    numbers()