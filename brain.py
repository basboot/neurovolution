# Based on code from
# https://towardsdatascience.com/lets-code-a-neural-network-in-plain-numpy-ae7e74410795
import numpy as np

def create_random_brain(nn_architecture, seed=None):
    if seed is not None:
        np.random.seed(seed)

    random_brain = []

    for idx, layer in enumerate(nn_architecture):
        layer_input_size = layer["input_dim"]
        layer_output_size = layer["output_dim"]

        random_brain += [np.random.random() * 1.0 for _ in range(layer_output_size * layer_input_size + layer_output_size)]



    return random_brain


def init_layers(nn_architecture, brain, seed=99):
    params_values = []

    brain_index = 0
    for idx, layer in enumerate(nn_architecture):
        layer_input_size = layer["input_dim"]
        layer_output_size = layer["output_dim"]

        W = np.reshape(brain[brain_index:brain_index + layer_output_size * layer_input_size], (layer_output_size, layer_input_size))
        b = np.reshape(brain[brain_index + layer_output_size * layer_input_size:brain_index + layer_output_size * layer_input_size + layer_output_size], (layer_output_size, 1))

        brain_index += layer_output_size * layer_input_size + layer_output_size
        layer_params = [W, b]

        params_values.append(layer_params)

    return params_values

def sigmoid(Z):
    return 1/(1+np.exp(-Z))

def relu(Z):
    return np.maximum(0,Z)

def sigmoid_backward(dA, Z):
    sig = sigmoid(Z)
    return dA * sig * (1 - sig)

def relu_backward(dA, Z):
    dZ = np.array(dA, copy = True)
    dZ[Z <= 0] = 0
    return dZ


def single_layer_forward_propagation(A_prev, W_curr, b_curr, activation="relu"):
    Z_curr = np.dot(W_curr, A_prev) + b_curr

    if activation == "relu":
        activation_func = relu
    elif activation == "sigmoid":
        activation_func = sigmoid
    else:
        raise Exception('Non-supported activation function')

    return activation_func(Z_curr), Z_curr


def full_forward_propagation(X, params_values, nn_architecture):
    A_curr = X

    for idx, layer in enumerate(nn_architecture):
        A_prev = A_curr

        activ_function_curr = layer["activation"]
        W_curr = params_values[idx][0]
        b_curr = params_values[idx][1]
        A_curr, Z_curr = single_layer_forward_propagation(A_prev, W_curr, b_curr, activ_function_curr)

    return A_curr

class Brain:
    def __init__(self, architecture, brain):
        self.params_values = init_layers(architecture, brain)
        self.architecture = architecture

    def forward_propagation(self, inputs):
        return full_forward_propagation(inputs, self.params_values, self.architecture)



if __name__ == '__main__':
    # test nn code
    nn_architecture = [
        {"input_dim": 2, "output_dim": 4, "activation": "relu"},
        {"input_dim": 4, "output_dim": 6, "activation": "relu"},
        {"input_dim": 6, "output_dim": 6, "activation": "relu"},
        {"input_dim": 6, "output_dim": 4, "activation": "relu"},
        {"input_dim": 4, "output_dim": 1, "activation": "sigmoid"},
    ]

    brain = create_random_brain(nn_architecture)
    params_values = init_layers(nn_architecture, brain)

    X = np.random.randn(2, 1)
    print(X)
    print(full_forward_propagation(X, params_values, nn_architecture))





