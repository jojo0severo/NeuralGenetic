import numpy as np


class NeuralNetwork:
    def __init__(self, layers, init_layers=True):
        if init_layers:
            self.weights, self.bias = self.__init_layers(layers)
        else:
            self.weights, self.bias = layers

        self.size = len(self.weights)

    def forward(self, x):
        current = np.array(x, dtype=float)
        for i in range(len(self.weights) - 1):
            current = self.activation(np.dot(current, self.weights[i]) + self.bias[i])

        return np.argmax(self.softmax(np.dot(current, self.weights[-1]) + self.bias[-1]), axis=1)[0]

    @staticmethod
    def __init_layers(layers):
        numpy_weight = []
        numpy_bias = []
        for input_size, output_size in layers:
            numpy_weight.append(np.random.random_integers(-1, high=1, size=(input_size, output_size)))
            numpy_bias.append(np.random.random_integers(-1, high=1, size=(1, output_size)).reshape(1, -1))

        return numpy_weight, numpy_bias

    @staticmethod
    def activation(x):
        return np.where(x >= 0,
                        1 / (1 + np.exp(-x)),
                        np.exp(x) / (1 + np.exp(x)))

    @staticmethod
    def softmax(x):
        x = np.exp(x - np.max(x))
        return x / x.sum()

    def __floordiv__(self, other):
        out_weights = []
        out_bias = []
        for i in range(self.size):
            out_weights.append(np.mean([self.weights[i], other.weights[i]], axis=0))
            out_bias.append(np.mean([self.bias[i], other.bias[i]], axis=0))

        return NeuralNetwork(layers=(out_weights, out_bias), init_layers=False)


if __name__ == '__main__':
    a = NeuralNetwork([(6, 8), (8, 8), (8, 4)])
    b = NeuralNetwork([(6, 8), (8, 8), (8, 4)])

    inpt = np.random.random_sample((1, 6)).reshape(1, -1)
    print(a.forward(inpt.tolist()))
