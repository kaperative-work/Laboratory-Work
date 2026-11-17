import numpy as np

stop_counts = {"pure": 0, "depth": 0, "gain": 0}


def build_tree(data, labels, depth=0, max_depth=MAX_DEPTH, min_samples_leaf=MIN_SAMPLES_LEAF):
    if len(np.unique(labels)) == 1:
        stop_counts["pure"] += 1
        return Leaf(data, labels)
    if depth >= max_depth:
        stop_counts["depth"] += 1
        return Leaf(data, labels)
    best_gain, t, index = find_best_split(data, labels, min_samples_leaf)
    if best_gain == 0:
        stop_counts["gain"] += 1
        return Leaf(data, labels)
    true_data, false_data, true_labels, false_labels = split(data, labels, index, t)
    true_branch = build_tree(true_data, true_labels, depth + 1, max_depth, min_samples_leaf)
    false_branch = build_tree(false_data, false_labels, depth + 1, max_depth, min_samples_leaf)
    return Node(index, t, true_branch, false_branch)


def classify_object(obj, node):
    if isinstance(node, Leaf):
        return node.prediction
    if obj[node.index] <= node.t:
        return classify_object(obj, node.true_branch)
    return classify_object(obj, node.false_branch)


def predict(data, tree):
    classes = []
    for obj in data:
        classes.append(classify_object(obj, tree))
    return np.asarray(classes)


def accuracy_metric(actual, predicted):
    actual = np.asarray(actual)
    predicted = np.asarray(predicted)
    return float(np.sum(actual == predicted) / len(actual))


def print_tree(node, spacing=""):
    if isinstance(node, Leaf):
        print(spacing + "Прогноз:", node.prediction, "объектов:", len(node.labels))
        return
    print(spacing + "Индекс", str(node.index), "<=", str(round(node.t, 4)))
    print(spacing + "--> True:")
    print_tree(node.true_branch, spacing + "  ")
    print(spacing + "--> False:")
    print_tree(node.false_branch, spacing + "  ")


my_tree = build_tree(X_train, y_train)
print("Остановы: чистый узел", stop_counts["pure"], ", глубина", stop_counts["depth"], ", нет прироста", stop_counts["gain"])
print_tree(my_tree)
