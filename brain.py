# Based on code from
# https://towardsdatascience.com/lets-code-a-neural-network-in-plain-numpy-ae7e74410795
import numpy as np

def create_random_brain(layers, nn_connections):
    nn_layers = {}
    for layer in layers:
        nn_layers[layer[0]] = layer[1:]

    random_brain = []
    for connection in nn_connections:

        layer_input_size = nn_layers[connection[0]][0]
        layer_output_size = nn_layers[connection[1]][0]

        random_brain += [np.random.random() * 1.0 for _ in range(layer_output_size * layer_input_size + layer_output_size)]

    return random_brain


def sigmoid(Z):
    return 1/(1+np.exp(-Z))

def relu(Z):
    return np.maximum(0,Z)


class Brain:
    def __init__(self, config, brain):
        self.config = config
        self.nn_layers, self.nn_connections, self.params_values = self.init_brain(brain)

    def init_brain(self, brain):
        layers = self.config['sensors']['functions'] + self.config['brain']['hidden_layers'] + self.config['actuators'][
            'functions']
        nn_layers = {}
        for layer in layers:
            nn_layers[layer[0]] = layer[1:]

        nn_connections = self.config['brain']['connections']

        params_values = []

        brain_index = 0
        for connection in nn_connections:
            layer_input_size = nn_layers[connection[0]][0]
            layer_output_size = nn_layers[connection[1]][0]

            W = np.reshape(brain[brain_index:brain_index + layer_output_size * layer_input_size],
                           (layer_output_size, layer_input_size))
            b = np.reshape(brain[
                           brain_index + layer_output_size * layer_input_size:brain_index + layer_output_size * layer_input_size + layer_output_size],
                           (layer_output_size, 1))

            brain_index += layer_output_size * layer_input_size + layer_output_size
            layer_params = [W, b]

            params_values.append(layer_params)

        return nn_layers, nn_connections, params_values

    def full_forward_propagation(self, inputs):
        # create memory for all layers, filled with sensor values and zeros
        memory = {}
        for layer_name, layer_params in self.nn_layers.items():
            memory[layer_name] = inputs[layer_name] if layer_name in inputs else np.zeros((layer_params[0], 1))

        for i in range(len(self.nn_connections)):
            connection = self.nn_connections[i]

            # get input from memory
            input = memory[connection[0]]

            # apply activation to input
            if self.nn_layers[connection[0]][1] == "relu":
                input = relu(input)
            elif self.nn_layers[connection[0]][1] == "sigmoid":
                input = sigmoid(input)
            else:
                pass
                # no activation

            W = self.params_values[i][0]
            b = self.params_values[i][1]
            output = np.dot(W, input) + b

            # add output to memory
            memory[connection[1]] += output

        # apply activation to all actuators and return values
        outputs = {}
        for actuator_name, _, actuator_activation, _ in self.config['actuators']['functions']:
            if actuator_activation == "relu":
                outputs[actuator_name] = relu(memory[actuator_name])
            elif actuator_activation == "sigmoid":
                outputs[actuator_name] = sigmoid(memory[actuator_name])
            else:
                outputs[actuator_name] = memory[actuator_name]

        # apply hardwired connections
        for direct_connection in self.config['brain']['direct_connections']:
            outputs[direct_connection[1]] = memory[direct_connection[0]]

        return outputs









