
from random import seed, random, randrange
from numpy import array

class NeuralNetwork():
    def __init__(self, row_size, dataset):
        self.row_size = row_size
        self.neurons = [{"weight": {'X':0, 'O':0, '0':0}, "items": {'X':0, 'O':0, '0':0}} for x in range(row_size * row_size)]
        self.dataset = dataset

    def train(self):
        for game in self.dataset:
            for turn, grid in enumerate(game['grids']):
                if game['player'] == 1:
                    grid = grid.replace('X', 'O')
                for i, box in enumerate(grid):
                    self.neurons[i]["items"][box] += 1
                    self.neurons[i]["weight"][box] = (self.neurons[i]["weight"][box] + game['moves'][turn + 1])
        print("Training Done !")
        print(self.neurons)        

    def add_to_dataset(self, data):
        self.dataset.append(data)

    def get_dataset(self):
        return self.dataset
        
    def get_next_move(self, grid):
        print("Given grid is ")
        print(grid)
        if "0" not in grid:
            return 0
        output = {"weight": 0, "items": 0}
        possible_moves = []
        for i, box in enumerate(grid):
            if self.neurons[i]['items'][box] == 0:
                print("[Warning] The neural network hasn't been trained for every input")
            else:
                neuron_choice = self.neurons[i]['weight'][box] / self.neurons[i]['items'][box];
                if grid[round(neuron_choice)] == '0':
                    possible_moves.append(round(neuron_choice))
                    print("Neuron choice : %s" %round(neuron_choice))
                    output['weight'] = output['weight'] + neuron_choice
                    output['items'] += 1
        if output['items'] != 0:
            move = int(round(output['weight'] / output['items']))
            if grid[move] == '0':
                output['weight'] /= output['items']
                print("AI has chosen ")
                print(output)
                return int(round(output['weight']))
            else:
                print("AI would have played %i but it was impossible" %move)
        print("Trying to return another one of the possible moves")
        if len(possible_moves):
            return possible_moves[randrange(0, len(possible_moves))]
        print("AI Couldn't find a smart move. Retuning a random move")
        while True:
            move = randrange(0, self.row_size * self.row_size)
            if grid[move] == '0':
                return move
