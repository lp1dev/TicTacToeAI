
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
                for i, box in enumerate(grid):
                    self.neurons[i]["items"][box] += 1
                    self.neurons[i]["weight"][box] = (self.neurons[i]["weight"][box] + game['moves'][turn + 1])
                    print("weight[%s][%i] : %s\nitems: %i" %(box, i,  self.neurons[i]["weight"][box], self.neurons[i]['items'][box]))
        print("Training Done !")
        print(self.neurons)        

    def get_next_move(self, grid):
        print("Given grid is ")
        print(grid)
        output = {"weight": 0, "items": 0}
        for i, box in enumerate(grid):
            if self.neurons[i]['items'][box] == 0:
                print("[Warning] The neural network hasn't been trained for every input")
            else:
                output['items'] += 1
                neuron_choice = self.neurons[i]['weight'][box] / self.neurons[i]['items'][box];
                print("Neuron choice : %s" %neuron_choice)
                output['weight'] = output['weight'] + neuron_choice
        output['weight'] /= output['items']
        print("AI has chosen ")
        print(output)
        return int(output['weight'])
