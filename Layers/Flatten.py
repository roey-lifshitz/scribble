from typing import Tuple
from Layers.Layer import Layer
import numpy as np

class Flatten(Layer):

    def __init__(self):
        self.input_shape = None

    def forward_propagate(self, inputs: np.ndarray) -> np.ndarray:
        """

        :param inputs: ND vector with shape of (n, ...., c)
        :return: 1D vector with shape of (n, 1)
        """
        self.input_shape = inputs.shape
        n = inputs.shape[0]
        return np.ravel(inputs).reshape(n, -1)

    def backward_propagate(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        """

        :param output_gradient: 1D vector with shape (n, 1)
        :param learning_rate: Not trainable so doesnt matter
        :return: ND vector with shape (n, ...., c)
        """
        return np.reshape(output_gradient, self.input_shape)
