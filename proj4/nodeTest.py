import random, math

data_entries = []
# The learning rate for the learn method
LEARNING_RATE = 0.5

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

    @staticmethod
    def sigmoid(z):
        return 1/(1 + math.exp(-z))

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
        for child in self.children:
            # Let the child know their parent, and the weight between them
            child[0].sayHiToDad(self, child[1])
            child[0].sayHiToTheKids()
    
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

        rows_sizes = rows_sizes[1:-1]        
        for num, rowSize in enumerate(rows_sizes):
            nextRow = []
            lastRow = (num == TOTAL_ROWS - 2)

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
                for cNode in nextRow:
                    randomWeight = random.uniform(-0.01, 0.01)
                    node.adoptChild(cNode, randomWeight)
            lastLayer = nextRow

        for node in self.topNodes:
            node.sayHiToTheKids()

    def train(self, inputs, expected):
        # Take this list of [0, 0, 4, 1]
        if (len(inputs) != len(self.leafNodes)-1):
            raise ValueError
        # Set the 4 leaf nodes to 0, 0, 4, and 1 (not forgetting the bias node)
        for i in range(1, len(self.leafNodes)):
            self.leafNodes[i].value = inputs[i-1]

        for i, topNode in enumerate(self.topNodes):
            topNode.updateNodeVal()
            topNode.backProp(expected[i])
        
        for topNode in self.topNodes:
            for child in topNode.children:
                child[0].backProp()
            topNode.learn()

    def test(self, inputs):
        if (len(inputs) != len(self.leafNodes)-1):
            raise ValueError
        
        for i in range(1, len(self.leafNodes)):
            self.leafNodes[i].value = inputs[i-1]

        for topNode in self.topNodes:
            topNode.updateNodeVal()

        return [endNodes.value for endNodes in self.topNodes]

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

def weather():
    read_examples("fishingNN.data")
    network = NeuralNet([1, 3, 5, total_attributes])
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