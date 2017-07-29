from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import tensorflow as tf
from sklearn.cross_validation import StratifiedKFold
import numpy as np
import glob
import os

def load_data(data_dir):
    img_width, img_height = 150, 150

    data_dir = os.path.expanduser(data_dir)

    label_names = []                  
    for r, d, files in os.walk(data_dir):
        for i in range(len(d)):
            label_names.append(d[i])

    sub_dirs = [x[0] for x in os.walk(data_dir)]
    dir_names = [os.path.basename(sub_dir) for sub_dir in sub_dirs]

    file_glob = [os.path.join(data_dir, dir_name, '*.jpeg') for dir_name in dir_names]
    
    file_list = []
    for i in range(1,len(file_glob)):
        file_list.extend(glob.glob(file_glob[i]))
        
    np.random.seed(7)
    np.random.shuffle(file_list)

    label_strings = [os.path.basename(os.path.dirname(file)) for file in file_list]

    labels = []
    for l in label_strings:
        if l == label_names[0]:
            labels.append(0)
        elif l == label_names[1]:
            labels.append(1)
        elif l == label_names[2]:
            labels.append(2)
        elif l == label_names[3]:
            labels.append(3)
        elif l == label_names[4]:
            labels.append(4)
        elif l == label_names[5]:
            labels.append(5)
        elif l == label_names[6]:
            labels.append(6)
        else:
            labels.append(7)
            
    data = []
    for file in file_list:
        img = load_img(file)  # this is a PIL image
        x = img_to_array(img, data_format='channels_first')
        data.append(x)
    
    data = np.asarray(data)
    labels = np.asarray(labels)[...,np.newaxis]
    return data, labels
    
def gen_train_test(data,labels):
    num_classes = 8
    
    x_test = data[0:int(20/100*len(data)),:,:,:]
    y_test = labels[0:int(20/100*len(labels)),:]
    
    x_train = data[int(20/100*len(data)),:,:,:]
    y_train = labels[0:int(20/100*len(labels)),:]
    
    y_train = np_utils.to_categorical(y_train, num_classes)
    y_test = np_utils.to_categorical(y_test, num_classes)
    
    return (x_train, y_train), (x_test, y_test)
