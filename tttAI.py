#!/bin/python

from sys import argv
from random import randrange
from neural_network import NeuralNetwork
from time import sleep
import pexpect
import json

encoding = 'UTF-8'
datasetfile = "dataset.json"
verbose = False

def usage():
  print("usage : %s program" %argv[0])
  return 0

def parse_output(child, turn):
  grid = ""
  done = False
  error = None
  while not done:
    line = child.readline().decode(encoding).strip()
    if len(line) <= 2:
      continue
    elif len(line) == 3:
        grid += line
    elif len(line) == 4:
        grid += line[1:]
    else:
      error = line
      return error, grid
    if len(grid) == 9:
      return error, grid
    
def play(child, grid):
  move = randrange(0, 9)
  if (verbose):
    print("Playing position %i" %move)
  child.sendline("%i" %move)
  return move
  
def play_alone(child):
  go_on = True
  turn = 0
  player = 1
  players_data = [{"player": 1, "moves":[], "grids":[]}, {"player": 2, "moves":[], "grids":[]}]
  last_move = None
  while go_on:
    if (verbose):
      print("Turn %i, player %i" %(turn, player))
    error, grid = parse_output(child, turn)
    if not error:
      player = 1 if player == 2 else 2
      if turn > 0:
        players_data[player - 1]['grids'].append(grid)
        players_data[player - 1]['moves'].append(last_move)
      if (verbose):
        print("Grid [%s]" %grid)
    else:
      if "Tie!" in error:
        if (verbose):
          print(error)
        return None
      elif "won!" in error:
        players_data[player - 1]['moves'].append(last_move)
        if (verbose):
          print(error)
        return players_data[player - 1]
      else:
        if (verbose):
          print("Error : [%s]" %error)
    last_move = play(child, grid)
    turn += 1

def save_dataset(data):
  with open(datasetfile, "w+") as f:
    f.write(json.dumps(data))
    
def train(games):
  games_data = []
  i = 0
  while i < games:
    child = pexpect.spawn(argv[1])
    data = play_alone(child)
    if data is not None:
      games_data.append(data)
      print("[%i/%i]" %(i + 1, games))
      i += 1
    child.close()
  print("Training on %i winning games done !" %games)
  print(games_data)
  return games_data
  
def	main():
  if (len(argv) != 2):
    return usage()
  games_data = train(2)
  save_dataset(games_data)
  nn = NeuralNetwork(3, games_data)

if __name__ == '__main__':
  main()
