import os, sys
from os.path import dirname, join, abspath

if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import random

from res.colors import *
from res.libs import *
import res.main as rm

flipsStyle = x.GREEN + "Flips" + x.END
headsStyle = x.YELLOW + "Heads" + x.END
tailsStyle = x.ORANGE + "Tails" + x.END
tieStyle = x.RED + "Tie" + x.END

heads = 0
tails = 0
flips = heads + tails
winner = None

def roll(num):
        
    heads = 0
    tails = 0
        
    for i in range(num):
        res = random.randint(0,1)
        if res:
            heads += 1
        else:
            tails += 1
                
    return [heads, tails]
    
def getNum():
    print(f"\n{x.YELLOW}>>>{x.VIOLET} How many times do you wanna flip the coin?")
    choice = input(intake.prompt)
    try:
        choice = rm.choice_check(choice)
    except:
        pass
        
    allowed = "1234567890"
    if go_thro(choice, allowed):
        
        if choice == '':
            clear()
            choice = getNum()
            
        choice = int(choice)
            
        if choice > 1000 or choice < 1:
            clear()
            output.invalid("Only numbers between 1:1000")
            getNum()
            
            
    else:
        clear()
        output.invalid("Only numbers between 1:1000")
        choice = getNum()
    return choice

def getStats(result):
    heads = result[0]
    tails = result[1]
    total = heads + tails

    headsPer = round(((heads/total)*100), 2)
    tailsPer = round(((tails/total)*100), 2)
    
    return [headsPer, tailsPer]

def resultDisplay(result, stats):
    global winner
    global heads
    global tails
    global flips
    
    heads = result[0]
    tails = result[1]
    flips = heads + tails
    headsPer = stats[0]
    tailsPer = stats[1]
    
    if heads > tails:
        winner = headsStyle
    elif heads < tails:
        winner = tailsStyle
    else:
        winner = tieStyle
        
    if headsPer % 1 == 0:
        headsPer = int(headsPer)
    if tailsPer % 1 == 0:
        tailsPer = int(tailsPer)
    
    clear()
    print(f"\n{x.YELLOW}>>>{x.VIOLET} Results:")
    print(f" {x.YELLOW}-{c.END} {x.GRAY}You rolled:{x.LETTUCE} {flips} {'times' if flips > 1 else 'time'}{c.END}")
    print(f" {x.YELLOW}-{c.END} {x.GRAY}Heads:{x.LETTUCE} {heads} {x.SKY}>> {x.LETTUCE}{headsPer}%{c.END}")
    print(f" {x.YELLOW}-{c.END} {x.GRAY}Tails:{x.LETTUCE} {tails} {x.SKY}>> {x.LETTUCE}{tailsPer}%{c.END}")
    print(f" {x.YELLOW}-{c.END} {x.GRAY}So {winner}{x.GRAY}, it is.{c.END}")
    
    enter_continue()

def flipeur():
    
    num = getNum()
    result = roll(num)
    stats = getStats(result)
    
    resultDisplay(result, stats)

if __name__ == "__main__":
    flipeur()
    #print(winner, heads, tails, flips, sep="\n")