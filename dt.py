import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import log, e
from dt_utils import *
import collections
sns.set()
import copy

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def find_split(df, feature, label):
    """ Given examples and feature, find best split"""
    #sort rows in df by value in column
    df = df.sort_values(by=[feature])

    # Find the points in change classes
    differ_list = ((df[label] != df[label].shift()) & (df[feature] != df[feature].shift()))
    differ_list[0] = False

    possible_splits_list = ((df.shift()[differ_list][feature] + df[differ_list][feature]) / 2).tolist()

    entropy_list = []
    for split in possible_splits_list:
        entropy_list.append(calc_split_ent(df, feature, label, split))

    if not entropy_list:
        return None, calc_ent(df[feature].tolist())

    best_entropy = min(entropy_list)
    best_split = possible_splits_list[entropy_list.index(best_entropy)]
    return best_split, best_entropy


def id3(df, label, depth=99999, count=0, majority=None):
    df = df.reset_index(drop=True)
    features = df.drop(label, axis=1).columns
    if count >= depth:
        return df[label].mode()[0]

    if df[label].nunique() == 1:
        return df[label][0]

    if df.empty:
        return majority

    majority = df[label].mode()[0]

    feature_choice = None
    split = None
    best_ent = 99999
    for feature in features:
        split_result = find_split(df, feature, label)
        if split_result[1] < best_ent:
            split = split_result[0]
            best_ent = split_result[1]
            feature_choice = feature

    if split == None:
        return majority

    df_less = df[df[feature_choice] < split]
    df_more = df[df[feature_choice] >= split]
    tree_less = id3(df_less, label, depth, count + 1, majority)
    tree_more = id3(df_more, label, depth, count + 1, majority)

    if tree_less == tree_more:
        tree = tree_less
    else:
        tree = {(feature_choice, split): {'less': tree_less, 'more': tree_more}}

    return tree

def depth(d, level=1):
    """ return max depth """
    if not isinstance(d, dict) or not d:
        return level
    return max(depth(d[k], level + 1) for k in d)


def classify(row, tree):
    """ given data, return class """
    if not isinstance(tree, dict):
        return tree
    feature = next(iter(tree))[0]
    split = next(iter(tree))[1]
    next_tree = tree[next(iter(tree))]

    if row[feature] < split:
        return classify(row, next_tree['less'])
    else:
        return classify(row, next_tree['more'])
    return

def calc_ent(labels):
    """ Given list of classes, return entropy """
    entropy = 0.
    n_labels = len(labels)
    if n_labels <= 1:
        return 0
    value, counts = np.unique(labels, return_counts=True)
    probs = counts / n_labels
    n_classes = np.count_nonzero(probs)

    #if all 0
    if n_classes <= 1:
        return 0

    for prob in probs:
        entropy -= prob * log(prob, 2)

    return entropy


def calc_split_ent(df, feature, label, split):

    more_than_labels = df[df[feature] >= split][label].tolist()
    less_than_labels = df[df[feature] < split][label].tolist()
    num_less = len(less_than_labels)
    num_more = len(more_than_labels)
    num_total = num_less + num_more
    return (((num_less / num_total) * (calc_ent(less_than_labels))) + ((num_more / num_total) * (calc_ent(more_than_labels))))

def get_k_fold_indices(df, n_splits=10):
    return k_fold(df, n_splits)

def compare_truth_and_prediction(df1,df2):
    same = len(df1.where(df1.values==df2.values))

    return same

def main():
    df = get_df()
    decision_tree = id3(df, 'class')
    pretty_print(decision_tree)

    # check if classification is 100%
    df_test = df.drop('class', axis=1)
    df_test['predicted_class'] = df_test.apply(lambda row: classify(row, decision_tree), axis=1)
    acc=compare_truth_and_prediction(df["class"], df_test['predicted_class'])
    print("Similarity between actual and predicted: "+ str(acc))

    X = df.drop('class', axis=1)
    kf = get_k_fold_indices(df, n_splits=10)

    df_accuracy = pd.DataFrame({
        'max_depth': np.arange(1,11),
        'avg_train_acc': np.zeros(10),
        'avg_test_acc': np.zeros(10)
    })
    #print(kf)
    for max_depth in range(10):
        train_acc = []
        test_acc = []
        for train_index, test_index in kf:
            df_train = df.iloc[train_index]
            df_test = df.iloc[test_index]
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]

            tree = id3(df_train, 'class', depth=max_depth)

            X_train['class'] = X_train.apply(lambda row: classify(row, tree), axis=1)
            X_test['class'] = X_test.apply(lambda row: classify(row, tree), axis=1)

            train_diff = pd.concat([X_train, df_train]).drop_duplicates(keep=False).shape[0] / 2
            train_acc.append((df_train.shape[0] - train_diff) / df_train.shape[0])
            test_diff = pd.concat([X_test, df_test]).drop_duplicates(keep=False).shape[0] / 2
            test_acc.append((df_test.shape[0] - test_diff) / df_test.shape[0])
        df_accuracy.loc[df_accuracy['max_depth'] == max_depth, 'avg_train_acc'] = sum(train_acc) / len(train_acc)
        df_accuracy.loc[df_accuracy['max_depth'] == max_depth, 'avg_test_acc'] = sum(test_acc) / len(test_acc)

    print(df_accuracy)

    plt.figure(figsize=(10, 10))
    plt.title('Avg predict acc on training set against max depth of the decision tree')
    plt.xlabel('Max depth of decision tree')
    plt.ylabel('Avg prediction acc on training set')
    plt.scatter(x='max_depth', y='avg_train_acc', data=df_accuracy)
    plt.savefig('data/train_results.png')
    plt.show()

    plt.figure(figsize=(10, 10))
    plt.title('Average prediction accuracy on validation set against maximum depth of the decision tree')
    plt.xlabel('Maximum depth of decision tree')
    plt.ylabel('Average prediction accuracy on validation set')
    plt.scatter(x='max_depth', y='avg_test_acc', data=df_accuracy)
    plt.savefig('data/test_results.png')
    plt.show()

    CHOSEN_DEPTH=3

    best_decision_tree = id3(df, 'class', depth=CHOSEN_DEPTH)
    pretty_print(best_decision_tree)

    df_test = df.drop('class', axis=1)
    df_test['class'] = df_test.apply(lambda row: classify(row, best_decision_tree), axis=1)
    differences = pd.concat([df,df_test]).drop_duplicates(keep=False).shape[0] / 2
    (df_test.shape[0] - differences) / df_test.shape[0]

if __name__ == "__main__":
    main()