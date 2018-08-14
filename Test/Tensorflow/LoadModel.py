from __future__ import absolute_import, division, print_function

import os

import tensorflow as tf 
from tensorflow import keras

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

new_model = tf.keras.models.load_model('my_model.h5')
new_model.summary()
loss, acc = new_model.evaluate(x_test, y_test)
print("Restored model, accuracy: {:5.2f}%".format(100*acc))