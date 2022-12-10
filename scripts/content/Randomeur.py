import sys
from os.path import abspath, dirname, join

# Sets path to the app's main folder
if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '../..')))

from scripts.libs import *



flipsStyle = X0.GREEN + "Flips" + X0.END
headsStyle = X0.YELLOW + "Heads" + X0.END
tailsStyle = X0.ORANGE + "Tails" + X0.END
tieStyle = X0.RED + "Tie" + X0.END

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
    print(f"\n{X0.YELLOW}>>>{X0.VIOLET} How many times do you wanna flip the coin?")
    choice = intake.prompt()
    if choice == "exit":
        print( "\033[1A" + output.notify("Oh, bye. :(", Print=False))
        enterContinue(False)
        clear()
        return

    allowed = "1234567890"
    if goThro(choice, allowed):

        if choice == '':
            clear()
            choice = getNum()

        choice = int(choice)

        if choice > 10000 or choice < 1:
            clear()
            output.error("Only numbers between 1:10000")
            getNum()

    else:
        clear()
        output.error("Only numbers between 1:10000")
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

    headsLen = len(str(heads))
    tailsLen = len(str(tails))
    tallrLen = headsLen if headsLen > tailsLen else tailsLen if tailsLen > headsLen else tailsLen
    totalLen = headsLen + tailsLen

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
    print(f"\n{X0.YELLOW}>>>{X0.VIOLET} Results:")
    print(f" {X0.YELLOW}-{C0.END} {X0.GRAY}You rolled:{X0.LETTUCE} {flips} {'times' if flips > 1 else 'time'}{C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {X0.GRAY}Heads: {X0.LETTUCE}{heads}{' ' * (tallrLen - headsLen)} {X0.SKY}>> {X0.LETTUCE}{headsPer}%{C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {X0.GRAY}Tails: {X0.LETTUCE}{tails}{' ' * (tallrLen - tailsLen)} {X0.SKY}>> {X0.LETTUCE}{tailsPer}%{C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {X0.GRAY}So {winner}{X0.GRAY}, it is.{C0.END}")

    enterContinue()

def flipeur():

    num = getNum()
    if num == None:
        return
    result = roll(num)
    stats = getStats(result)

    resultDisplay(result, stats)

if __name__ == "__main__":
    flipeur()
    #print(winner, heads, tails, flips, sep="\n")
