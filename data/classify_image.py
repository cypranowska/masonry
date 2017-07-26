'''
Modified tensorflow example code from http://github.com/eldor4do
https://github.com/eldor4do/TensorFlow-Examples/blob/master/retraining-example.py

run_inference_on_images takes as input the path to a model,
path to the file with labels, and a list of paths to image files
and then classifies each image with one of the labels 
according to the best score from the models

'''

import tensorflow as tf
import numpy as np


def create_graph(modelFullPath):
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

def run_inference_on_images(modelFullPath, labelsFullPath, imagePaths):
    answer = None
    pred_labels = []

    #if not tf.gfile.Exists(imagePath):
    #    tf.logging.fatal('File does not exist %s', imagePath)
    #    return answer

    # Creates graph from saved GraphDef.
    create_graph(modelFullPath)

    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        for i in imagePaths:
            image_data = tf.gfile.FastGFile(i, 'rb').read()
            predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)

            top_k = predictions.argsort()[-5:][::-1]  # Getting top 5 predictions

            f = open(labelsFullPath, 'r')
            lines = f.readlines()
            labels = [str(w).strip() for w in lines]
            answer = labels[top_k[0]]
            pred_labels.append(answer)

    return pred_labels


if __name__ == '__main__':

    modelFullPath = '/tmp/output_graph.pb'
    labelsFullPath = '/tmp/output_labels.txt'
    images = ['../../../flower_photos/daisy/21652746_cc379e0eea_m.jpg',
              '../../../flower_photos/dandelion/17280886635_e384d91300_n.jpg']

    list_of_labels = run_inference_on_images(modelFullPath,
                                            labelsFullPath,
                                            images)

    print(list_of_labels)
