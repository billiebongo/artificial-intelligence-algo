
import numpy as np
import pandas as pd
import copy
from random import shuffle
import itertools


def get_df():
    df = pd.read_csv('data/set_a.csv', names=['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class'])
    df['class'] = pd.to_numeric(df['class'], downcast='integer').astype('category')
    df.head()
    return df

def pretty_print(tree, depth=0):
    """ print tree with """
    if isinstance(tree, dict):
        feature = next(iter(tree))[0]
        split = next(iter(tree))[1]
        next_tree = tree[next(iter(tree))]
        print('{}{} < {}'.format(' ' * depth * 3, feature, str(round(split,2))))
        pretty_print(next_tree['less'], depth + 1)
        print('{}{} > {}'.format(' ' * depth * 3, feature, str(round(split,2))))
        pretty_print(next_tree['more'], depth + 1)
    else:
        print('{} is classified into Class {}'.format(' ' * depth * 3, tree))


def k_fold(df, k):
    rows = list(range(df.shape[0]))
    shuffle(rows)
    multi = int(df.shape[0] / k)

    folds = []
    for fold in range(k):
        folds.append(rows[(fold * multi):((fold * multi) + multi)])

    train_test_indexes = []
    for i in range(len(folds)):
        all_folds = copy.deepcopy(folds)
        test_index = folds.pop(i)
        train_index = list(itertools.chain.from_iterable(folds))
        train_test_indexes.append((train_index, test_index))
        folds = copy.deepcopy(all_folds)

    return train_test_indexes

