from random import seed, random, randrange
from numpy import array

class NeuralNetwork():
    def __init__(self, row_size, dataset):
        self.row_size = row_size
        self.neurons = [0 for x in range(row_size)]
        self.dataset = dataset
