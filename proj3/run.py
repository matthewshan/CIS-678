import math

meta_data = {
    "classes": [],
    "attr": {
        # "wind": (0, ["Strong", "Weak"])
    }
}

def generate_next_nodes(data_set, root_node):
    # Check and see if we can set a value for our root node, ie. stop recursively calling
    all_same_class = True
    class_type = data_set[0][-1]
    # If all the entries share the same class (True/False) then set the parent node to that?
    for entry in data_set:
        if (entry[4] != class_type):
            # Not all the entries are the same type, so all_same_class shouldn't be true
            all_same_class = False
    if (all_same_class):
        # set val
        root_node = class_type
        return

    # TODO We also need to check if there are no more attributes to test

    # Otherwise, we're going to generate our next decision node
    best_attribute = ""
    best_gain = 0.0
    for attr in meta_data["attr"]:
        attr_gain = calculate_gain(data_set, attr)
        if (attr_gain > best_gain):
            best_gain = attr_gain
            best_attribute = attr
    # We now know the best attribute and it's gain value, so that's our next decision
    # Now we must generate a node for each possible value of that attribute
    attr_values = meta_data["attr"][best_attribute][1]
    attr_pos = meta_data["attr"][best_attribute][0]
    for attr_val in attr_values:
        sub_data = []
        # Create sub data sets for each value of the attribute
        for entry in data_set:
            if (entry[attr_pos] == attr_val):
                sub_data.append(entry)
        # Add nodes. For each new node, call recursively to generate its own child nodes    
        # Root --> Water --> Hot
        # Root --> Water --> Cold
        if (len(sub_data) != 0):
            root_node[best_attribute][attr_val] = generate_next_nodes(sub_data, root_node[best_attribute][attr_val])
    # Everything should be generated at this point, so all done
    return

#Calculates the entropy of the given attribute.
#Leave blank to get the entropy of the whole set_data
def calculate_entropy(data_set, attr=None, attr_value=None):
    result = 0
    # Calculates the entropy of the given attribute value
    if attr is not None and attr_value is not None :
        attr_index = meta_data["attr"][attr][0]
        for cl in meta_data["classes"]:
            # Number of data with the given attr_value and the given class
            num_cl = len(list(filter(lambda example: example[attr_index] == attr_value and data_set[-1] == cl, data_set)))
            # Number of data with the given attr_value
            num_attr = len(list(filter(lambda example: example[attr_index] == attr_value, data_set)))
            if num_attr != 0:
                p_cl = num_cl/num_attr
            else:
                p_cl = 0 #Unsure?
            if p_cl != 0:
                result += p_cl * math.log2(p_cl)
    #Entropy of ALL the data
    else:
        for cl in meta_data["classes"]:
            # Number of data of given class
            num_cl = len(list(filter(lambda example: data_set[-1] == cl, data_set)))
            # Number of data with the given attr_value
            num_attr = len(data_set)
            p_cl = num_cl/num_attr
            if p_cl != 0:
                result += p_cl * math.log2(p_cl)
            
    return result
        

def calculate_gain(data_set, attr):
    result = calculate_entropy(data_set)
    attr_index = meta_data["attr"][attr][0]
    for value in meta_data["attr"][attr][1]:
        len_value = len(list(filter(lambda example: example[attr_index] == value, data_set)))
        len_set = len(data_set)
        result -= (len_value/len_set) * calculate_entropy(data_set, attr, value)
    return result
        

def generate_metadata(file_name):
    my_file = open(file_name)
    # Skip the first line
    my_file.readline()
    # Read in the possible classes from the second line
    classes = my_file.readline().split(",")
    meta_data["classes"] = classes

    # Read the third line, aka the total number of attributes
    total_attr = my_file.readline()
    # Read in each attribute and it's possible values
    for attr in range(int(total_attr)):
        attr_values = my_file.readline().split(",")
        meta_data["attr"][attr_values[0]] = tuple((attr, attr_values[2:]))
    my_file.close()

def read_examples(file_path):
    total_num_lines = 0
    data_list = []
    file = open(file_path)
    for line in file:
        #print (line)
        # Skip the lines until you find the 3rd only-number line.
        if (len(line) < 5):
            total_num_lines += 1
        # Find the 3rd line that is just a number. All the lines after that are training data.
        elif (total_num_lines >= 3):
            # Arrived at data section in file, so start adding lists
            # ex. [ Strong,Warm,Warm,Sunny,Yes ]
            data_entry = line.split(",")
            data_list.append(data_entry)
    print(total_num_lines)
    file.close()
    return data_list

# Read in the training examples
data_list = read_examples("fishing.data")
# Read in the possible classes and attributes
generate_metadata("fishing.data")
decision_tree = {}
generate_next_nodes(data_list, decision_tree)