#!/bin/python

from sys import argv
from random import randrange
from modules.average_network import AverageNetwork
from time import sleep
from os.path import isfile
import pexpect
import json

encoding = 'UTF-8'
datasetfile = "dataset1.json"
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

def user_play(child, grid, an):
  move_str = ''
  while len(move_str) == 0:
    move_str = input("move : ")
  move = int(move_str)
  if (verbose):
    print("User playing position %i" %move)
  child.sendline("%i" %move)
  return move
    
def ai_play(child, grid, an):
  move = an.get_next_move(grid)
  if (verbose):
    print("AI playing position %i" %move)
  child.sendline("%i" %move)
  return move

    
def random_play(child, grid, an):
  move = randrange(0, 9)
  if (verbose):
    print("AI playing position %i" %move)
  child.sendline("%i" %move)
  return move

def print_grid(grid):
  for i, box in enumerate(grid):
    if box == "0":
      print("%i|" %i,end='')
    else:
      print("%s|" %box,end='')
    if ((i + 1) % 3) == 0:
      print()

def generic_play(an, player1, player2):
  child = pexpect.spawn(argv[1])  
  go_on = True
  turn = 0
  player = 1
  players_data = [{"player": 1, "moves":[], "grids":[]}, {"player": 2, "moves":[], "grids":[]}]
  last_move = None
  last_grid = None
  while go_on:
    if (verbose):
      print("Turn %i, player %i" %(turn, player))
    error, grid = parse_output(child, turn)
    if not error:
      last_grid = grid
      if turn > 0:
        player = 1 if player == 2 else 2
        players_data[player - 1]['grids'].append(grid)
        players_data[player - 1]['moves'].append(last_move)
      if (verbose):
        print_grid(grid)
    else:
      if "Tie!" in error:
        if (verbose):
          print(error)
        return None
      elif "won!" in error:
        winner = int(error[8:9])
        players_data[winner - 1]['moves'].append(last_move)
        if (verbose):
          print(error)
        return players_data[winner - 1]
      else:
        if (verbose):
          print("Error : [%s]" %error)
    if player == 2:
      last_move = player2(child, last_grid, an)
    else:
      last_move = player1(child, last_grid, an)
    turn += 1
      
def save_dataset(data):
  with open(datasetfile, "w+") as f:
    f.write(json.dumps(data))

def load_dataset():
  with open(datasetfile) as f:
    raw = f.read()
    dataset = json.loads(raw)
    print("Loaded %i entries from %s" %(len(dataset), datasetfile))
    return dataset
    
def random_train(games):
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
  print("Random training on %i winning games done !" %games)
  print(games_data)
  return games_data

def train(games):
  games_data = []
  i = 0
  while i < games:
    data = play_vs_random()
    if data is not None:
      games_data.append(data)
      print("[%i/%i]" %(i + 1, games))
      i += 1
  print("Random training on %i winning games done !" %games)
  print(games_data)
  return games_data

def continuous_train(an):
  games_data = []
  while True:
    data = generic_play(an, ai_play, user_play)
#    data = generic_play(an, user_play, ai_play)
    print(data)
    an.add_to_dataset(data)
    save_dataset(an.get_dataset())

def	main():
  if (len(argv) != 2):
    return usage()
  games_data = []
  if (isfile(datasetfile)):
    answer = input('There is an existing %s file, do you want to override it ? :[y/n]' %datasetfile)
    if answer and answer[0].lower() == 'y':
      save_dataset(games_data)
    else:
      games_data = load_dataset()
  an = AverageNetwork(3, games_data)
  an.train()
  continuous_train(an)

if __name__ == '__main__':
  main()
