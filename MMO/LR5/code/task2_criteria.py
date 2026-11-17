import numpy as np


class Node:
    def __init__(self, index, t, true_branch, false_branch):
        self.index = index
        self.t = t
        self.true_branch = true_branch
        self.false_branch = false_branch


class Leaf:
    def __init__(self, data, labels):
        self.data = data
        self.labels = labels
        self.prediction = self.predict()

    def predict(self):
        classes = {}
        for label in self.labels:
            if label not in classes:
                classes[label] = 0
            classes[label] += 1
        return max(classes, key=classes.get)


def gini(labels):
    labels = np.asarray(labels)
    if len(labels) == 0:
        return 0.0
    _, counts = np.unique(labels, return_counts=True)
    shares = counts / len(labels)
    return float(1.0 - np.sum(shares ** 2))


def gain(left_labels, right_labels, root_gini):
    n_left = len(left_labels)
    n_right = len(right_labels)
    n = n_left + n_right
    if n_left == 0 or n_right == 0:
        return 0.0
    p_left = n_left / n
    return root_gini - p_left * gini(left_labels) - (1.0 - p_left) * gini(right_labels)


def split(data, labels, column_index, t):
    left = np.where(data[:, column_index] <= t)
    right = np.where(data[:, column_index] > t)
    true_data = data[left]
    false_data = data[right]
    true_labels = labels[left]
    false_labels = labels[right]
    return true_data, false_data, true_labels, false_labels


def find_best_split(data, labels, min_samples_leaf=MIN_SAMPLES_LEAF):
    root_gini = gini(labels)
    best_gain = 0.0
    best_t = None
    best_index = None
    n_features = data.shape[1]
    for index in range(n_features):
        values = np.unique(data[:, index])
        for i in range(len(values) - 1):
            t = (float(values[i]) + float(values[i + 1])) / 2.0
            _, _, true_labels, false_labels = split(data, labels, index, t)
            if len(true_labels) < min_samples_leaf or len(false_labels) < min_samples_leaf:
                continue
            current_gain = gain(true_labels, false_labels, root_gini)
            if current_gain > best_gain:
                best_gain, best_t, best_index = current_gain, t, index
    return best_gain, best_t, best_index


print("Джини обучения:", round(gini(y_train), 6))
print("Джини чистого узла:", gini(np.array([0, 0, 0])))
print("Джини узла 50/50:", gini(np.array([0, 1])))
