
# ID3
import pandas as pd


class DecisionTree():
    tree = {}

    def learn(self, training_set, features, target):
        self.tree = ID3(features, examples)


# Class Node which will be used while classify a test-instance using the tree which was built earlier
class Node():
    value = "" # lower or higher
    children = []

    def __init__(self, val, dictionary):
        self.value = val
        if (isinstance(dictionary, dict)):
            self.children = dictionary.keys()

def print_tree(tree):
    return

def find_split_point():
    #split point is chosen based on max gain in entropy

    return_split_point


# Majority Function which tells which class has more entries in given data-set
def choose_majority_class(features, data, target):
    freq = {}
    index = features.index(target)

    for tuple in data:
        if (freq.has_key(tuple[index])):
            freq[tuple[index]] += 1
        else:
            freq[tuple[index]] = 1

    max = 0
    major = ""

    for key in freq.keys():
        if freq[key] > max:
            max = freq[key]
            major = key

    return major


# Calculates the entropy of the data given the target attribute
def calc_entropy(features, data, targetAttr):
    """ features """
    freq = {}
    entropy = 0.0

    i = 0
    for feature in features:
        if (targetAttr == features):
            break
        i = i + 1

    i = i - 1

    #classifying the datra
    for row in data:
        if (freq.has_key(row[i])):
            freq[entry[i]] += 1.0
        else:
            freq[entry[i]] = 1.0

    for prob in freq.values():
        entropy += (-prob/ len(data)) * math.log(prob / len(data), 2)

    return entropy


def get_best_split_point(data, index_of_attribute_to_sort_by):
    #sort the list of lists by value at index of inner list
    index_of_attribute_to_sort_by =

    sorted_data=sorted(data, key=lambda row: row[4])

    for row in data:


    return possible_split_points


# Calculates the information gain (reduction in entropy) in the data when a particular attribute is chosen for splitting the data.
def info_gain(features, data, attr, targetAttr):


    freq = {}
    after_class_entropy = 0.0
    i = features.index(attr)

    # sorts rows in data acc to the value in the col of attr
    for f_index in range(len(features)):
        best_split_point = get_possible_split_points(data, )

    for row in data:
        if (freq.has_key(row[i])):
            freq[row[i]] += 1.0
        else:
            freq[row[i]] = 1.0

    for val in freq.keys():
        prob = freq[val] / sum(freq.values())
        dataSubset = [entry for entry in data if entry[i] == val]
        after_class_entropy += prob * calc_entropy(features, dataSubset, targetAttr)
    info_gain = entropy(features, data, targetAttr) - after_class_entropy
    return info_gain




# This function chooses the attribute among the remaining features which has the maximum information gain.
def choose_best_feature(data, features, target):
    best = features[0]
    maxGain = 0;

    for attr in features:
        #for each feature order the values for that feature.
        newGain = info_gain(features, data, attr, target)
        if newGain > maxGain:
            maxGain = newGain
            best = attr

    return best


# This function will get unique values for that particular attribute from the given data
def get_values(data, features, attr):
    index = features.index(attr)
    values = []

    for entry in data:
        if entry[index] not in values:
            values.append(entry[index])

    return values


# This function will get all the rows of the data where the chosen "best" attribute has a value "val"
def get_data(data, features, best, val):
    new_data = [[]]
    index = features.index(best)

    for entry in data:
        if (entry[index] == val):
            newEntry = []
            for i in range(0, len(entry)):
                if (i != index):
                    newEntry.append(entry[i])
            new_data.append(newEntry)

    new_data.remove([])
    return new_data


# This function is used to build the decision tree using the given data, features and the target features. It returns the decision tree in the end.
def ID3(examples, features):

    examples= examples[:]

    # list of all classes of data
    classes = [row[features.index(target)] for row in data]

    #if all in the same class
    if len(set(classes)):
        print("all of the same class")
        return classes[0]

    #if no more examples or features
    if not data or (len(features) - 1) <= 0:
        return default
    #if all data of the same class
    elif classes.count(classes[0]) == len(classes):
        return classes[0]
    #
    else:
        best = choose_best_feature(data, features, target)
        tree = {best: {}}

        for val in get_values(data, features, best):
            new_data = get_data(data, features, best, val)
            newAttr = features[:]
            newAttr.remove(best)
            subtree = build_tree(new_data, newAttr, target)
            tree[best][val] = subtree

    return tree

import csv
# This function runs the decision tree algorithm. It parses the file for the data-set, and then it runs the 10-fold cross-validation. It also classifies a test-instance and later compute the average accurracy
# Improvements Used:
# 1. Discrete Splitting for features "age" and "fnlwght"
# 2. Random-ness: Random Shuffle of the data before Cross-Validation
def run_decision_tree():
    data = []
    with open("data/set_a.csv") as csvfile:

        for line in csv.reader(csvfile, delimiter=","):
            print(type(line))
            data.append(line)

    features = ['sepal_length', 'sepal_width' , 'petal_length', 'petal_width', 'class']
    target = features[-1]

    #for k in range(K):
        #random.shuffle(data)
        #training_set = [x for i, x in enumerate(data) if i % K != k]
        #test_set = [x for i, x in enumerate(data) if i % K == k]
    training_set=data
    tree = DecisionTree()
    tree.learn(training_set, features, target)


if __name__ == "__main__":
    run_decision_tree()


