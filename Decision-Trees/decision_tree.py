import numpy as np
from collections import Counter

#Single tree node class that takes the arguments:
#-feature index, split threshold for a feature, 
#-left and right son 
#-and a value (if it is a leaf)
#it has a method that cheks if a node is a leaf
class Node:
  def __init__(self, feature=None, threshold=None, left=None, right=None,*, value=None): 
    self.feature = feature
    self.threshold = threshold
    self.left = left
    self.right = right
    self.value = value

  def is_leaf_node(self):
    return self.value is not None

#DecisionTree clas that has the arguments:
#-Minimal samples to split
#-Maximal depth of the tree
#-Number of features that are chosen during the split
#-Root 
class DecisionTree:
  def __init__(self, min_samples_split=2, max_depth=100, n_features=None):
    self.min_samples_split=min_samples_split
    self.max_depth=max_depth
    self.n_features=n_features
    self.root=None

#Method that makes the tree out of X values 
#(counted as lengths of rows, passed as a tree's argument )
# and y as tree values
#It works by setting the features number as a length of X shape if it's not present or a minimum of both
# n_features and length of column
# lastly it "grows" the tree
  def fit(self, X, y): 
    if self.n_features is None:
        self.n_features = len(X[0])
    else:
        self.n_features = min(self.n_features, len(X[0]))
    self.root = self._grow_tree(X, y)

#Method that makes the tree recursively
#It uses the sample and feature count and number of different values
  def _grow_tree(self, X, y, depth=0):
    n_samples = len(X)
    n_features = len(X[0])
    n_labels = len(np.unique(y))

    # checks the following criteria : maximum depth, the amount of samples is to small, there is one value left
    # takes the most common value for the leaf and returns the node with the value
    if depth >= self.max_depth or n_samples < self.min_samples_split or n_labels == 1:
      counter = Counter(y)
      most_common_value = counter.most_common(1)[0][0]
      return Node(value=most_common_value)
    
    #takes random indexes for the features
    feat_idxs = np.random.choice(n_features, self.n_features, replace=False)
    best_gain = -1
    split_index = None 
    split_threshold = None
    #loops through the features and finds the best split point based on the information
    for i in feat_idxs:
        values = X[:, i]
        thresholds = np.unique(values)

        for j in range(1, len(thresholds)):
            middle_threshold = (thresholds[j] + thresholds[j - 1]) / 2
            info_gain = self._information_gain(y, values, middle_threshold)

            if info_gain > best_gain:
                best_gain = info_gain
                split_index = i
                split_threshold = middle_threshold

    #once it has been found, the method splits the data into left and right subsets based on the selected feature and threshold 
    #and it recursively calls itself to grow the left and right subtrees 
    left_indexes, right_indexes = self._split(X[:, split_index], split_threshold)
    left = self._grow_tree(X[left_indexes], y[left_indexes], depth + 1)
    right = self._grow_tree(X[right_indexes], y[right_indexes], depth + 1)
    #returns the root node of the decision tree
    return Node(split_index, split_threshold, left, right)

#Method that finds the best splits for the given data sets
  def _best_split(self, X, y, feat_idxs):
      split_index = None
      split_threshold = None
      best_gain = -1
      for i in feat_idxs:
          values = X[:, i]
          unique_values = np.unique(values)
          if len(unique_values) == 1:
              continue  # cannot split on a feature with only one unique value
          for threshold in unique_values[:-1]:
              gain = self._information_gain(y, values, threshold)
              if gain > best_gain:
                  best_gain = gain
                  split_index = i
                  split_threshold = threshold
      return split_index, split_threshold

#method that calculates the information gain for a given feature and a threshold value
#it calculates the entropy of y target values using the _enthropy method
#splits the X_column into two sets based on threshold value using the boolean mask
#it returns zero if it's empty, if not it calculates the entropy of left and right subsets and weights them by the proportion of samples in subsets
#and return the total entropy of the two subsets after the split
  def _information_gain(self, y, X_column, threshold):
    parent_entropy = self._entropy(y)
    left_mask = X_column <= threshold
    left_indexes = np.where(left_mask)[0]
    right_indexes = np.where(~left_mask)[0]

    if len(left_indexes) == 0 or len(right_indexes) == 0:
        return 0
  
    left_entropy = self._entropy(y[left_indexes])
    right_entropy = self._entropy(y[right_indexes])
    count = len(y)
    left_weight = len(left_indexes) / count
    right_weight = len(right_indexes) / count
    children_entropy = left_weight * left_entropy + right_weight * right_entropy
    return parent_entropy - children_entropy

#method that splits the sets and return two arrays which represent the indexes that belongs to both of them
  def _split(self, X_column, split_thresh):
    left_indexes = []
    right_indexes = []
    for i, x in enumerate(X_column):
        if x <= split_thresh:
            left_indexes.append(i)
        else:
            right_indexes.append(i)
    return np.array(left_indexes), np.array(right_indexes)

  def _entropy(self, y):
    hist = np.bincount(y)
    ps = hist / len(y)
    return -np.sum([p * np.log(p) for p in ps if p>0])

#method that traverses the tree
  def _traverse_tree(self, x, node):
    if node.is_leaf_node():
      return node.value
    
    if x[node.feature] <= node.threshold:
      return self._traverse_tree(x,node.left)
    else:
      return self._traverse_tree(x,node.right)

#method that makes predictions based on a tree that was made
  def predict(self, X):
    return np.array([self._traverse_tree(x, self.root) for x in X])