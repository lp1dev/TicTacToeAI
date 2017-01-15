#!/bin/python

from sys import argv
from random import randrange
from neural_network import NeuralNetwork
from time import sleep
from os.path import isfile
import pexpect
import json

encoding = 'UTF-8'
datasetfile = "dataset.json"
verbose = True

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

def user_play(child, grid):
  move = int(input("move : "))
  if (verbose):
    print("User playing position %i" %move)
  child.sendline("%i" %move)
  return move

    
def ai_play(child, grid, nn):
  move = nn.get_next_move(grid)
  if (verbose):
    print("AI playing position %i" %move)
  child.sendline("%i" %move)
  return move

    
def random_play(child, grid):
  move = randrange(0, 9)
  if (verbose):
    print("AI playing position %i" %move)
  child.sendline("%i" %move)
  return move

def play(nn):
  child = pexpect.spawn(argv[1])  
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
    if player == 2 and len(grid):
      last_move = ai_play(child, grid, nn)
    else:
      last_move = user_play(child, grid)
    turn += 1

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
    last_move = random_play(child, grid)
    turn += 1

def save_dataset(data):
  with open(datasetfile, "w+") as f:
    f.write(json.dumps(data))

def load_dataset():
  with open(datasetfile) as f:
    raw = f.read()
    return json.loads(raw)
    
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
  if (isfile(datasetfile)):
    answer = input('There is an existing dataset.json file, do you want to override it ? :[y/n]')
    if answer and answer[0].lower() == 'y':
      games_data = train(25)
      save_dataset(games_data)
    else:
      games_data = load_dataset()
  nn = NeuralNetwork(3, games_data)
  nn.train()
  play(nn)

if __name__ == '__main__':
  main()
