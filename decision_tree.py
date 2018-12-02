
# ID3
import pandas as pd


class DecisionTree():
	tree = {}

	def learn(self, training_set, features, target):
		self.tree = ID3(features, examples)


# Class Node which will be used while classify a test-instance using the tree which was built earlier
class Node():
	value = "" #class
	children = []

	def __init__(self, class, children):
		self.class = class
		if (isinstance(dictionary, dict)):
			self.children = children



def get_f_index(feature):
	return ['sepal_length', 'sepal_width' , 'petal_length', 'petal_width'].index(feature)

# Majority Function which tells which class has more entries in given data-set
def choose_majority_class(examples, features):
	freq = {}

	for row in examples:
		if (freq.has_key(row[-1])):
			freq[row] += 1
		else:
			freq[row] = 1

	majority_class = max(freq, key=freq.get)

	return majority_class


# Calculates the entropy of the data given the target attribute
def calc_entropy(c0_count, c1_count, c2_count):
	""" Assuminh 3 classes """
	total=c1_count+c2_count+c3_count
	#classifying the datra
	#for row in data:
	#    if (freq.has_key(row[i])):
	#        freq[entry[i]] += 1.0
	#    else:
	#        freq[entry[i]] = 1.0


	entropy = (-c0_count/ total) * math.log(c0_count / total, 2) + (-c1_count/ total) * math.log(c1_count/ total, 2) + (-c2_count/ total) * math.log(c2_count/ total, 2)

	return entropy

def calc_info_gain(current_entropy, splitting_point, feature,examples ):
	"""split the examples and return the info gain"""


	f_index = get_f_index(feature)

	after_class_entropy = 0
	for i in range(2):
		if i==0:
			#less than

			subset_examples = [e for e in examples if e[f_index]<splitting_point]
			prob = len(subset_examples) / len(examples)
		else:
			#more than

			subset_examples = [e for e in examples if e[f_index] > splitting_point]
			prob = len(subset_examples) / len(examples)
		c0_count = 0
		c1_count = 0
		c2_count = 0
		for row in subset_examples:
			if (str(row[-1])==str('0.0')):
				c0_count +=1

			if str(row[-1])==str('1.0'):
				c1_count +=1

			if str(row[-1])==str('2.0'):
				c2_count +=1
		after_class_entropy +=  prob* calc_entropy(c0_count, c1_count, c2_count)

	info_gain = current_entropy - after_class_entropy
	return info_gain


def get_info_gain_for_feature(f, examples):
	""" find best split point for feature """
	f_index=get_f_index(f)
	# sort by valye of that feature
	sorted_data = sorted(data, key=lambda row: row[f_index])
	possible_split_points=[]
	prev_row_class=examples[0][-1]
	for row in examples:
		if row[-1] != prev_row_class:
			possible_split_points.append((row[f_index]+prev_row_f_value)/2)
		prev_row_f_value=row[f_index]
	max_possible_split_info_gain_value = 0
	max_possible_splitting_point= 0

	# FINDING THE BEST SPLIT POINT

	#current
	c0= len([e for e in examples if str(e[-1])==str('0.0')])
	c1= len([e for e in examples if str(e[-1])==str('1.0')])
	c2= len([e for e in examples if str(e[-1])==str('2.0')])
	curr_entropy = calc_entropy()

	for possible_split_point in possible_split_points:
		info_gain = calc_info_gain(current_entropy, possible_splitting_point, f,examples )
		if info_gain>max_possible_split:
			max_possible_splitting_point= possible_split_point
			max_possible_split_info_gain_value = info_gain

	return max_possible_split_info_gain_value, max_possible_splitting_point







# This function chooses the attribute among the remaining features which has the maximum information gain.
def choose_best_feature(examples, features, current_entropy):
	best_feature = features[0]
	max_info_gain = 0
	best_feature_splitting_point=0

	# find best feature and respective splitting point
	for f in features:


		# i need thge feature and their respective info_gain
		new_info_gain, splitting_point = get_info_gain_for_feature(f, features, examples)

		if new_info_gain > max_info_gain:
			max_info_gain = new_info_gain
			best_feature_splitting_point=splitting_point
            best_feature=f


	return best_feature, splitting_point


# This function will get unique values for that particular attribute from the given data
def get_values(data, features, attr):
	index = features.index(attr)
	values = []

	for entry in data:
		if entry[index] not in values:
			values.append(entry[index])

	return values




# This function is used to build the decision tree using the given data, features and the target features. It returns the decision tree in the end.
def ID3(examples, features):


	# list of all classes of data
	classes = [row[-1] for row in examples]

	#if all in the same class
	if len(set(classes))==1: #classes.count(classes[0]) == len(classes):
		print("all of the same class")
		return Node(classes[0], examples)

	#if no more features, choose majority function
	elif (len(features) - 1) <= 0:
		return Node(choose_majority_class(examples, features), examples)
	#if no more examples, but still got features, return leaf node with majority decision of parent node
	elif len(examples)==0:
		print("no examples!")
		return Node(choose_parent_class, examples)

	else:
        best_feature, splitting_point=choose_best_feature(examples, features, current_entropy)
        #split examples with spliting point

		f_index = get_f_index(best_feature)
		less_than_examples=[]
		more_than_examples=[]
		for row in examples:
			if row[f_index] < splitting_point:
				less_than_examples.append(row)


		subtree_1 = ID3(less_than_examples, features)
		for row in examples:
			if row[f_index] >= splitting_point:
				more_than_examples.append(row)
		#assuming splitting pt can nvr be below -1
		subtree_2 = ID3(more_than_examples, features)


		tree = {best_feature:{-1:subtree_1,splitting_point: subtree_2}}


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


