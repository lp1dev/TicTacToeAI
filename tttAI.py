#!/bin/python

from sys import argv
from random import randrange
from time import sleep
import pexpect

encoding = 'UTF-8'
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
    
def play(child, grid):
  move = randrange(0, 9)
  if (verbose):
    print("Playing position %i" %move)
  child.sendline("%i" %move)
  
def game_input(child):
  go_on = True
  turn = 0
  player = 1
  while go_on:
    if (verbose):
      print("Turn %i, player %i" %(turn, player))
    error, grid = parse_output(child, turn)
    if not error:
      player = 1 if player == 2 else 2
      print("Grid [%s]" %grid)
    else:
      if "won!" in error or "Tie!" in error:
        print(error)
        break
      else:
        print("Error : [%s]" %error)
    play(child, grid)
    turn += 1

def	main():
  if (len(argv) != 2):
    return usage()
  child = pexpect.spawn(argv[1])
  game_input(child)

if __name__ == '__main__':
  main()
