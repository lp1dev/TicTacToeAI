from random import seed, random, randrange
from numpy import array

class NeuralNetwork():
    def __init__(self, row_size, dataset):
        self.row_size = row_size
        self.neurons = [0 for x in range(row_size * row_size)]
        self.dataset = dataset
        self.train()

    def train(self):
        for game in self.dataset:
            if game['player'] == 1:
                player_symbol = 'X'
            else:
                player_symbol = 'O'
            for turn, grid in enumerate(game['grids']):
                for i, box in enumerate(grid):
                    if box == player_symbol:
                        self.neurons[i] = (self.neurons[i] + game['moves'][turn + 1])/2
        print("Training Done !")
        print(self.neurons)
        
