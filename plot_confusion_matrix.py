import matplotlib.pyplot as plt
import numpy as np
import itertools
from sklearn.metrics import confusion_matrix

# Plots a confusion matrix
# Inputs:
#     - y_true: list of ground truth labels
#     - y_pred: list of predicted labels
#     - normalize (default=False): Normalizes count by true label
#     - filename (default=confusion_matrix.png): filename for figure
def plot_confusion_matrix(y_true,y_pred, normalize=False, filename='confusion_matrix.png'):
    cm_array = confusion_matrix(y_true,y_pred)
    if normalize:
        cm_array = cm_array.astype('float') / cm_array.sum(axis=1)[:, np.newaxis]

    true_labels = np.unique(y_true)
    pred_labels = np.unique(y_pred)
    fig = plt.figure(figsize=(8, 8))

    plt.imshow(cm_array, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Confusion matrix", fontsize=16)
    cbar = plt.colorbar(fraction=0.046, pad=0.1)

    colorscale_label = 'Number of images'
    if normalize:
        colorscale_label = 'Normalized # of images'
    cbar.set_label(colorscale_label, rotation=270, labelpad=15, fontsize=12)
    xtick_marks = np.arange(len(true_labels))
    ytick_marks = np.arange(len(pred_labels))
    plt.xticks(xtick_marks, true_labels, rotation=90)
    plt.yticks(ytick_marks,pred_labels)

    plt.ylabel('True label', fontsize=14)
    plt.xlabel('Predicted label', fontsize=14)

    thresh = cm_array.max() / 2.
    for i, j in itertools.product(range(cm_array.shape[0]), range(cm_array.shape[1])):
        if normalize:
            numstr = '%.2f' % cm_array[i, j]
        else:
            numstr = cm_array[i, j]
        plt.text(j, i, numstr,
                 horizontalalignment="center",
                 color="white" if cm_array[i, j] > thresh else "black")

    fig.tight_layout()
    fig.savefig(filename)

