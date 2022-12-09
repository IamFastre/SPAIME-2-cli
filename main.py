####################################################################
##                                                                ##
##    Importing important files, modules, packages and so on.     ##
##                                                                ##
####################################################################

import os, sys, random, shutil, subprocess, time, pickle, re
from datetime import datetime, date

# Importing the other py files.
from res.colors import *
from res.codes import *
from res.libs import *
from time import *

#==================================================================#

# Importing the applets
import scripts.TicTacToe            as ttt
import scripts.RockPaperScissors    as rps
import scripts.Randomeur            as rnd
import scripts.Minesweeper          as msp
import scripts.Blackjack            as bjk
import scripts.Sudoku               as sdk
import scripts.BrainfuckInterpreter as bfi

#==================================================================#

# Other python modules that will need pip'ing
try:
    import yaml
except ModuleNotFoundError:
    clear()
    output.warn(f"You seem to be missing the PyYAML module.")
    output.warn(f"Don't worry it's safe, gonna PIP it for you.")

    if confirm(output.warn(f"Download it?", Print=False)):
        pipInstall('pyyaml')
    else:
        output.error(f"OK, then.")
        exit(0)

    output.success(f"Now everything is good. If the app does't run (Specially If Unix/Linux), please just restart.")
    sleep(5)
finally:
    import yaml

#==================================================================#






####################################################################
##                                                                ##
## Loading the YAML & Pickle files and defining their functions.  ##
##                                                                ##
####################################################################


def readYAML():
    # Makes it re-read the YAML files
    global settings
    global user
    global apps
    global YAMLS

    with open('./data/settings.yml', 'rb') as SETTINGS:
        settings = yaml.safe_load(SETTINGS)

    with open('./data/user.yml', 'rb') as USER:
        user     = yaml.safe_load(USER)

    with open('./data/apps.yml', 'rb') as APPS:
        apps     = yaml.safe_load(APPS)

    YAMLS = (settings, user, apps)

readYAML()

#==================================================================#

def writeYAML():
    # Makes it write the YAML files
    global settings
    global user
    global apps
    global YAMLS

    with open('./data/settings.yml', 'w') as SETTINGS:
        yaml.dump(settings, SETTINGS)

    with open('./data/user.yml', 'w') as USER:
        yaml.dump(user, USER)

    with open('./data/apps.yml', 'w') as APPS:
        yaml.dump(apps, APPS)

    readYAML()

#==================================================================#

def resetYAML(YAML = None):
    # Resets YAML files
    global settings
    global user
    global apps
    global YAMLS

    if YAML != None:
        i = YAMLS.index(YAML)

        if i == 0:
            shutil.copy('./data/.default/settings.yml', './data/')
        if i == 1:
            shutil.copy('./data/.default/user.yml', './data/')
        if i == 2:
            shutil.copy('./data/.default/apps.yml', './data/')
    else:
        for file in glob.glob('./data/.default/*.yml'):
            shutil.copy(file, './data/')

    readYAML()

#==================================================================#

def resetTTT():
    # Resets TicTacToes in apps.yml
    global apps
    apps['ttt'] = {'last-board': ['—'] * 9, 'last-winner': '—', 'x-wins': 0, 'o-wins': 0, 'ties': 0, 'diff': 'M'}
    writeYAML()

#==================================================================#

def resetRPS():
    # Resets RockPaperScissors in apps.yml
    global apps
    apps['rps'] = {'p1': {'wins': 0, 'last-choice': '—'}, 'p2': {'wins': 0, 'last-choice': '—'}, 'cpu': {'wins': 0, 'last-choice': '—'}, 'ties': 0, 'last-winner': '—'}
    writeYAML()

#==================================================================#

def resetRND():
    # Resets Randomeur in apps.yml
    global apps
    apps['rnd'] = {'ties': 0, 'heads': 0, 'tails': 0, 'flips': 0, 'last-heads': 0, 'last-tails': 0, 'last-flips': 0, 'last-winner': '—'}
    writeYAML()

#==================================================================#

def resetMSP():
    # Resets Minesweeper in apps.yml
    global apps
    apps['msp'] = {'wins': 0, 'defeats': 0, 'spots-dug': 0, 'bombC': 10, 'dim': 10}
    resetPICKLE(mspBD)
    writeYAML()

#==================================================================#

def resetBJK():
    # Resets BlackJack in apps.yml
    global apps
    apps['bjk'] = {'balance': 500, 'soft-17': False, 'last-bet': 0, 'reward': '000000'}
    writeYAML()

#==================================================================#

def resetSDK():
    # Resets Sudoku in apps.yml
    global apps
    apps['sdk'] = {'wins': 0, 'empty': 35, 'validated': 0}
    resetPICKLE(sdkBD)
    writeYAML()

#==================================================================#

def readPICKLE():
    global mspBD
    global sdkBD
    global PICKLES

    with open('./data/mspBD.pkl', 'rb') as MSPBD:
        mspBD = pickle.load(MSPBD)

    with open('./data/sdkBD.pkl', 'rb') as SDKBD:
        sdkBD = pickle.load(SDKBD)

    PICKLES = (mspBD, sdkBD)

#==================================================================#

def writePICKLE():
    global mspBD
    global sdkBD
    global PICKLES

    with open('./data/mspBD.pkl', 'wb') as MSPBD:
        pickle.dump(mspBD, MSPBD)

    with open('./data/sdkBD.pkl', 'wb') as SDKBD:
        pickle.dump(sdkBD, SDKBD)

    readPICKLE()

#==================================================================#

def resetPICKLE(PICKLE = None):
    global mspBD
    global sdkBD
    global PICKLES

    if PICKLE != None:
        i = PICKLES.index(PICKLE)

        if i == 0:
            shutil.copy('./data/.default/mspBD.pkl', './data/')

        if i == 1:
            shutil.copy('./data/.default/sdkBD.pkl', './data/')

    else:
        for file in glob.glob('./data/.default/*.pkl'):
            shutil.copy(file, './data/')

    readPICKLE()

#==================================================================#

readYAML()
readPICKLE()

#==================================================================#






####################################################################
##                                                                ##
## Defining some useful functions, variables and other constants. ##
##                                                                ##
####################################################################

window = None
windowHistory = [window]

bricks = "{}"

today   = datetime.now().strftime("%y%m%d")
settings['last-date'] = today

admins = (f"fastre", "neria", "mahmoud")
passes = (576957, None)

placeholders = {
    'nl'            : '{' + 'nl' + '}',
    'br'            : '{' + 'br' + '}',

    'name'          : '{' + 'name' + '}',
    'age'           : '{' + 'age' + '}',

    'prefix'        : '{' + 'prefix' + '}',

    'lastTTTWinner' : '{' + 'lastTTTWinner' + '}',
    'lastTTTBoard'  : '{' + 'lastTTTBoard' + '}',
    'xWins'         : '{' + 'xWins' + '}',
    'oWins'         : '{' + 'oWins' + '}',
    'tttTies'       : '{' + 'tttTies' + '}',

    'g'             : '{' + 'g' + '}',
    'pi'            : '{' + 'pi' + '}',
    'e'             : '{' + 'e' + '}',
    'tau'           : '{' + 'tau' + '}',
    'phi'           : '{' + 'phi' + '}',

    'p1Last'   : '{' + 'p1Last' + '}',
    'p1Wins'   : '{' + 'p1Wins' + '}',
    'p2Last'   : '{' + 'p2Last' + '}',
    'p2Wins'   : '{' + 'p2Wins' + '}',
    'cpuLast'   : '{' + 'cpuLast' + '}',
    'cpuWins'   : '{' + 'cpuWins' + '}',
    'lastRPSWinner'   : '{' + 'lastRPSWinner' + '}',
    'rpsTies'   : '{' + 'rpsTies' + '}',

    'heads'   : '{' + 'heads' + '}',
    'tails'   : '{' + 'tails' + '}',
    'flips'   : '{' + 'flips' + '}',
    'rndTies'   : '{' + 'rndTies' + '}',
    'lastHeads'   : '{' + 'lastHeads' + '}',
    'lastTails'   : '{' + 'lastTails' + '}',
    'lastFlips'   : '{' + 'lastFlips' + '}',
    'lastRNDWinner'   : '{' + 'lastRNDWinner' + '}',

    'mspWins'   : '{' + 'mspWins' + '}',
    'mspDefeats'   : '{' + 'mspDefeats' + '}',
    'mspDug'   : '{' + 'mspDug' + '}',
    'mspBombs'   : '{' + 'mspBombs' + '}',
    'mspSize'   : '{' + 'mspSize' + '}',

    ''   : '{' + '' + '}',
}

writeYAML()

#==================================================================#

def isAdmin():
    return (user['name'].casefold() in admins and user['age'] in passes and user['sex'] == "Male")

#==================================================================#

def isCommand(thing):
    global commands

    commands = [
        settings['prefix'] + "help",
        settings['prefix'] + "help math",
        settings['prefix'] + "help rnd",
        settings['prefix'] + "help rps",
        settings['prefix'] + "help ttt",
        settings['prefix'] + "help msp",
        settings['prefix'] + "help bjk",
        settings['prefix'] + "help sdk",

        settings['prefix'] + "back",
        settings['prefix'] + "home",
        settings['prefix'] + "exit",
        settings['prefix'] + "refr",

        settings['prefix'] + "dev1",
        settings['prefix'] + "dev2",

        settings['prefix'] + "reset",
    ]

    if thing in commands:
        return True
    return False

#==================================================================#

class decoded():

    n69 = asciiToChar(f"80 97 114 108 101 115 45 116 117 32 100 101 32 115 101 120 101 32 63 32 59 41")
    n70 = asciiToChar(f"73 32 115 101 101 44 32 121 111 117 32 100 105 114 116 121 32 109 105 110 100 101 100 32 105 103 110 111 114 97 109 117 115 32 114 117 115 116 105 99 46")

    def f69():

        if random.randint(0,1) == 1:
            if user['name'] == '':
                print(f"\n{X0.YELLOW}>> {X0.VIOLETBG}{C0.WHITE}{decoded.n69}{C0.END}")
            else:
                print(f"\n{X0.YELLOW}>>{X0.GREEN} {user['name']}{C0.END}, {X0.VIOLETBG}{C0.WHITE}{decoded.n69}{C0.END}")
        else:
            if user['name'] == '':
                print(f"\n{X0.YELLOW}>> {X0.VIOLETBG}{C0.WHITE}{decoded.n70}{C0.END}")
            else:
                print(f"\n{X0.YELLOW}>>{X0.GREEN} {user['name']}{C0.END}, {X0.VIOLETBG}{C0.WHITE}{decoded.n70}{C0.END}")
        sleep(0.2)
        clear()

    def foo(force=False):
        if True or force:
            pass

#==================================================================#

def update():
    readYAML()
    readPICKLE()

#==================================================================#

def back(num = -1):
    WN = windowHistory[num]
    func = f"{WN}Menu()"

    update()

    try:
        exec(func)
    except ValueError:
        clear()
        output.error("I guess there's nothing to go back to.")
        back()
    except NameError:
        clear()
        output.notify("Hello, Hello!!")
        mainMenu()

#==================================================================#

def updateWindow(string):
    """Tell the app to change the window for the back() function."""
    global window
    global windowHistory

    window = string
    if window == windowHistory[-1]:
        pass
    else:
        windowHistory.append(string)
    
    update()

#==================================================================#

def choiceCheck(thing:str):
    """Makes changes to the input to execute commands or place the placeholders."""


    # Placeholders:
    if "{" in thing and "}" in thing:
        if placeholders['nl'] in thing:
            thing = thing.replace(placeholders['nl'], f"\n{X0.YELLOW}>>{X0.VIOLET}=============================={X0.YELLOW}<<{C0.END}\n{X0.VIOLET}>>{X0.GRAY} ")
        if placeholders['br'] in thing:
            thing = thing.replace(placeholders['br'], "\n" + output.notify(f"", Print = False) + X0.GRAY)

        if placeholders['name'] in thing:
            thing = thing.replace(placeholders['name'], str(user['name']))
        if placeholders['age'] in thing:
            thing = thing.replace(placeholders['age'], str(user['age']))

        if placeholders['prefix'] in thing:
            thing = thing.replace(placeholders['prefix'], str(settings['prefix']))

        if placeholders['lastTTTWinner'] in thing:
            thing = thing.replace(placeholders['lastTTTWinner'], str(apps['ttt']['last-winner']) + X0.GRAY) 
        if placeholders['xWins'] in thing:
            thing = thing.replace(placeholders['xWins'], str(apps['ttt']['x-wins']) + X0.GRAY)
        if placeholders['oWins'] in thing:
            thing = thing.replace(placeholders['oWins'], str(apps['ttt']['o-wins']) + X0.GRAY)
        if placeholders['tttTies'] in thing:
            thing = thing.replace(placeholders['tttTies'], str(apps['ttt']['ties']) + X0.GRAY)
        if placeholders['lastTTTBoard'] in thing:
            thing = thing.replace(placeholders['lastTTTBoard'], f"\n{ttt.displayBoard(apps['ttt']['last-board'], True, left=f'{X0.VIOLET}>>{C0.END} ')}{X0.VIOLET}>>{X0.GRAY} ")

        if placeholders['p1Last'] in thing:
            thing = thing.replace(placeholders['p1Last'], str(apps['rps']['p1']['last-choice']) + X0.GRAY)
        if placeholders['p2Last'] in thing:
            thing = thing.replace(placeholders['p2Last'], str(apps['rps']['p2']['last-choice']) + X0.GRAY)
        if placeholders['cpuLast'] in thing:
            thing = thing.replace(placeholders['cpuLast'], str(apps['rps']['cpu']['last-choice']) + X0.GRAY)
        if placeholders['p1Wins'] in thing:
            thing = thing.replace(placeholders['p1Wins'], str(apps['rps']['p1']['wins']) + X0.GRAY)
        if placeholders['p2Wins'] in thing:
            thing = thing.replace(placeholders['p2Wins'], str(apps['rps']['p2']['wins']) + X0.GRAY)
        if placeholders['cpuWins'] in thing:
            thing = thing.replace(placeholders['cpuWins'], str(apps['rps']['cpu']['wins']) + X0.GRAY)
        if placeholders['rpsTies'] in thing:
            thing = thing.replace(placeholders['rpsTies'], str(apps['rps']['ties']) + X0.GRAY)
        if placeholders['lastRPSWinner'] in thing:
            thing = thing.replace(placeholders['lastRPSWinner'], str(apps['rps']['last-winner']) + X0.GRAY)

        if placeholders['heads'] in thing:
            thing = thing.replace(placeholders['heads'], str(apps['rnd']['heads']) + X0.GRAY)
        if placeholders['tails'] in thing:
            thing = thing.replace(placeholders['tails'], str(apps['rnd']['tails']) + X0.GRAY)
        if placeholders['flips'] in thing:
            thing = thing.replace(placeholders['flips'], str(apps['rnd']['flips']) + X0.GRAY)
        if placeholders['rndTies'] in thing:
            thing = thing.replace(placeholders['rndTies'], str(apps['rnd']['ties']) + X0.GRAY)
        if placeholders['lastHeads'] in thing:
            thing = thing.replace(placeholders['lastHeads'], str(apps['rnd']['last-heads']) + X0.GRAY)
        if placeholders['lastTails'] in thing:
            thing = thing.replace(placeholders['lastTails'], str(apps['rnd']['last-tails']) + X0.GRAY)
        if placeholders['lastFlips'] in thing:
            thing = thing.replace(placeholders['lastFlips'], str(apps['rnd']['last-flips']) + X0.GRAY)
        if placeholders['lastRNDWinner'] in thing:
            thing = thing.replace(placeholders['lastRNDWinner'], str(apps['rnd']['last-winner']) + X0.GRAY)

        if placeholders['g'] in thing:
            thing = thing.replace(placeholders['g'], "9.8")
        if placeholders['e'] in thing:
            thing = thing.replace(placeholders['e'], "2.7182")
        if placeholders['pi'] in thing:
            thing = thing.replace(placeholders['pi'], "3.1415")
        if placeholders['tau'] in thing:
            thing = thing.replace(placeholders['tau'], "6.2830")
        if placeholders['phi'] in thing:
            thing = thing.replace(placeholders['phi'], "1.618")

        if placeholders['mspWins'] in thing:
            thing = thing.replace(placeholders['mspWins'], str(apps['msp']['wins']))
        if placeholders['mspDefeats'] in thing:
            thing = thing.replace(placeholders['mspDefeats'], str(apps['msp']['defeats']))
        if placeholders['mspDug'] in thing:
            thing = thing.replace(placeholders['mspDug'], str(apps['msp']['spots-dug']))
        if placeholders['mspBombs'] in thing:
            thing = thing.replace(placeholders['mspBombs'], str(apps['msp']['bombC']))
        if placeholders['mspSize'] in thing:
            thing = thing.replace(placeholders['mspSize'], str(apps['msp']['dim']))

        if placeholders[''] in thing:
            thing = thing.replace(placeholders[''], "")

    #==============================================================#

    # Easter Eggs:
    if "SPAIME" in thing:
        thing = thing.replace("SPAIME", f"{X0.YELLOW}[{X0.VIOLET}SPAIME{X0.YELLOW}]" + X0.GRAY)
    if "SPAIME-2" in thing:
        thing = thing.replace("SPAIME-2", f"{X0.YELLOW}[{X0.VIOLET}SPAIME{X0.YELLOW}]²" + X0.GRAY)
    if "Shrek" in thing:
        thing = thing.replace("Shrek", X0.GREEN + "Shrek" + X0.GRAY)

    #==============================================================#

    if thing == "":
        clear()
        output.error(f"You gotta type something first, no?")
        back()

    #==============================================================#

    # Commands:
    if thing.startswith(settings['prefix']):
        cmd = thing.replace(settings['prefix'], "")

        if not isCommand(thing):
            clear()
            output.error(f"Invalid command.")
            back()

        if cmd == "help":
            clear()
            helpF()
            back()
        if cmd == "help math":
            clear()
            helpMathF()
            back()
        if cmd == "help rnd":
            clear()
            helpRNDF()
            back()
        if cmd == "help rps":
            clear()
            helpRPSF()
            back()
        if cmd == "help ttt":
            clear()
            helpTTTF()
            back()
        if cmd == "help msp":
            clear()
            helpMSPF()
            back()
        if cmd == "help bjk":
            clear()
            helpBJKF()
            back()
        if cmd == "help sdk":
            clear()
            helpSDKF()
            back()


        if cmd == "back":
            clear()
            back(-2)
        if cmd == "home":
            clear()
            mainMenu()
        if cmd == "exit":
            exitF()
        if cmd == "refr":
            refreshF()


        if cmd == "dev1":

            if isAdmin():
                clear()

                def debug1():
                    print(f"\n{X0.ORANGE}>>>{X0.VIOLET} Hey boss! What do you wish to do?{C0.END}")
                    dev = input(f"\n{X0.ORANGE}1 >{X0.LETTUCE} ")
                    print(C0.END)

                    try:
                        print(eval(dev))
                        print("")
                    except NameError:
                        output.error(f"IDK WTF You did, maybe {settings['prefix']}dev again.")
                        enterContinue()
                        clear()
                        output.error(f"IDK WTF You did, maybe {settings['prefix']}dev again.")
                        back()
                    except SyntaxError:
                        output.error(f"IDK WTF You did, maybe {settings['prefix']}dev again.")
                        enterContinue()
                        clear()
                        output.error(f"IDK WTF You did, maybe {settings['prefix']}dev again.")
                        back()
                    else:
                        debug1()

                debug1()

            else:
                clear()
                output.error("It's a dev-only commands, buddy.")
                back()

        if cmd == "dev2":

            if isAdmin():
                clear()

                def debug1():
                    print(f"\n{X0.ORANGE}>>>{X0.VIOLET} Hey boss! What do you wish to do?{C0.END}")
                    dev = input(f"\n{X0.ORANGE}2 >{X0.LETTUCE} ")
                    print(C0.END)

                    try:
                        print(exec(dev))
                        print("")
                    except NameError:
                        output.error(f"IDK WTF You did, maybe {settings['prefix']}dev again.")
                        enterContinue()
                        clear()
                        output.error(f"IDK WTF You did, maybe {settings['prefix']}dev again.")
                        back()
                    except SyntaxError:
                        output.error(f"IDK WTF You did, maybe {settings['prefix']}dev again.")
                        enterContinue()
                        clear()
                        output.error(f"IDK WTF You did, maybe {settings['prefix']}dev again.")
                        back()
                    else:
                        debug1()

                debug1()

            else:
                clear()
                output.error("It's a dev-only commands, buddy.")

    return thing

#==================================================================#

def lastCheck(choice):
    if not isCommand(choice):
        output.error(f"Invalid input.")
    back()

#==================================================================#






####################################################################
##                                                                ##
##               The main app menu and app selector.              ##
##                                                                ##
####################################################################


def mainMenu():
    updateWindow(f"main")

    print()
    if user['name'] in ('', None):
        output.stamp(f"Hey there! Whatcha wanna do?!")
    else:
        output.stamp(f"Hey there, {X0.GREEN}{user['name']}{X0.VIOLET}! Whatcha wanna do?!")
    output.note(1, settings['prefix'])
    print()

    output.option("R", f"{X0.GRAY}[{X0.LETTUCE}↑↓{X0.GRAY}] {C0.URL}R{C0.END}{X0.GRAY}epeat")
    output.option("M", f"{X0.GRAY}[{X0.LETTUCE}π*{X0.GRAY}] {C0.URL}M{C0.END}{X0.GRAY}ath & Logic")
    output.option("A", f"{X0.GRAY}[{X0.ORANGE}¾{X0.YELLOW}%{X0.GRAY}] R{C0.URL}a{C0.END}{X0.GRAY}ndomeur")
    output.option("O", f"{X0.GRAY}[{X0.LETTUCE}$${X0.GRAY}] R{C0.URL}o{C0.END}{X0.GRAY}ckPaperScissors")
    output.option("T", f"{X0.GRAY}[{ttt.s.x}{ttt.s.o}{X0.GRAY}] {C0.URL}T{C0.END}{X0.GRAY}icTacToe")
    output.option("I", f"{X0.GRAY}[{msp.flagS}{msp.bombS}{X0.GRAY}] M{C0.URL}i{C0.END}{X0.GRAY}nesweeper")
    output.option("B", f"{X0.GRAY}[{bjk.suitS['H']}{bjk.suitS['S']}{X0.GRAY}] {C0.URL}B{C0.END}{X0.GRAY}lackJack")
    output.option("S", f"{X0.GRAY}[{X0.YELLOW}✎{X0.VIOLET}#{X0.GRAY}] {C0.URL}S{C0.END}{X0.GRAY}udoku")
    output.option("F", f"{X0.GRAY}[{X0.LETTUCE}+{X0.ORANGE}.{X0.GRAY}] Brain{C0.URL}F{C0.END}{X0.GRAY}uck")
    output.option("P", f"{X0.GRAY}[{X0.YELLOW}{bricks}{X0.GRAY}] O{C0.URL}p{C0.END}{X0.GRAY}tions")
    output.option("C", f"{X0.GRAY}[{X0.VIOLET}>>{X0.GRAY}] {C0.URL}C{C0.END}{X0.GRAY}redits")
    output.option("E", f"{X0.GRAY}[{X0.RED}x{X0.GREEN}✓{X0.GRAY}] {C0.URL}R{C0.END}{X0.GRAY}efresh")
    output.option("X", f"{X0.GRAY}[{X0.RED}xx{X0.GRAY}] E{C0.URL}x{C0.END}{X0.GRAY}it")

    choice = intake.prompt()
    choice = choiceCheck(choice)

    # El Menus
    if choice.upper() in ("1", "R", "REPEAT"):
        clear()
        repeatMenu()
    if choice.upper() in ("2", "M", "MATH"):
        clear()
        mathMenu()
    if choice.upper() in ("3", "A", "RND"):
        clear()
        rndMenu()
    if choice.upper() in ("4", "O", "RPS"):
        clear()
        rpsMenu()
    if choice.upper() in ("5", "T", "TTT"):
        clear()
        tttMenu()
    if choice.upper() in ("6", "I", "MSP"):
        clear()
        mspMenu()
    if choice.upper() in ("7", "B", "BJK"):
        clear()
        bjkMenu()
    if choice.upper() in ("8", "S", "SDK"):
        clear()
        sdkMenu()
    if choice.upper() in ("9", "F", "BFI"):
        clear()
        bfiMenu()
    if choice.upper() in ("10", "P", "OPTIONS"):
        clear()
        optionsMenu()
    if choice.upper() in ("11", "C", "CREDITS"):
        clear()
        infoF()
    if choice.upper() in ("12", "E", "REFRESH"):
        clear()
        refreshF()
    if choice.upper() in ("0", "X", "EXIT"):
        clear()
        exitF()

    if not(isCommand(choice)):
        clear()
        output.error(f"Invalid input.")
        back()

    clear()
    output.warn(f"Huh...")
    back()

#==================================================================#






####################################################################
##                                                                ##
##                        Other app menus.                        ##
##                                                                ##
####################################################################


def repeatMenu():
    updateWindow(f"repeat")

    print()
    output.stamp(f"What do you want me to repeat?")
    output.note(1, settings['prefix'])

    choice = intake.prompt()
    choice = choiceCheck(choice)

    if choice.casefold() == "idk" or choice.casefold() == "not sure":
        clear()
        output.error(f"Well, Why even ask?!")
    elif choice.casefold() == "fuck you":
        clear()
        output.error(f"No, you ↪.")
    elif choice == "69" or (f"sex" in choice.casefold()):
        decoded.f69()
        clear()
        output.notify(choice)
    else:
        clear()
        output.notify(choice)

    back(-2)

#==================================================================#

def mathMenu():
    updateWindow(f"math")

    print()
    output.stamp(f"Oh wanna do some math'ing?")
    output.note(1, settings['prefix'])

    choice = intake.prompt()
    choice = choiceCheck(choice)
    choice = choice.replace("^", "**").replace("x", "*").replace("×", "*").replace("÷", "/").replace("\\", "/")
    choiceL = choice.split("#")
    choice  = choiceL[0]

    allowed = "0123456789+-*/.,()%=TF!&| "
    if goThro(choice,allowed):
        choice  = choice.replace("!", "not ").replace("not =", "!=").replace("&", " and ").replace("|", " or ").replace("T", " True ").replace("F", " False ")

        try:
            choice = eval(choice)
        except:
            clear()
            output.error(f"That's not really math or logic...")
        else:
            if choice == 69:
                decoded.f69()
            clear()
            try:
                choice = str(choice).replace("True", "T").replace("False", "F")
            except:
                output.error("Woah, cowboy! Easy on your machine.")
            else:
                output.notify(choice)
    else:
        clear()
        output.error(f"That's not really math or logic...")

    back()

#==================================================================#

def rndMenu():
    updateWindow(f"rnd")

    def statsMenu():
        print()
        output.stamp(f"Randomeur Statistics:\n")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total {rnd.headsStyle}{C0.END}: {X0.GRAY}{apps['rnd']['heads']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total {rnd.tailsStyle}{C0.END}: {X0.GRAY}{apps['rnd']['tails']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total {rnd.flipsStyle}{C0.END}: {X0.GRAY}{apps['rnd']['flips']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total {rnd.tieStyle}{X0.RED}s{C0.END}:  {X0.GRAY}{apps['rnd']['ties']}{C0.END}")
        print(f"")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last {rnd.headsStyle}{C0.END}:  {X0.GRAY}{apps['rnd']['last-heads']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last {rnd.tailsStyle}{C0.END}:  {X0.GRAY}{apps['rnd']['last-tails']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last {rnd.flipsStyle}{C0.END}:  {X0.GRAY}{apps['rnd']['last-flips']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last Winner{C0.END}: {X0.GRAY}{apps['rnd']['last-winner']}{C0.END}")
        enterContinue()

    def statsReset():
        if confirm(output.notify(f"Are you sure?", Print= False)):
            resetRND()
            clear()
            output.success(f"All done, good as new.")
            back()
        else:
            clear()
            output.error(f"Okay then.")
            back()

    print()
    output.stamp(f"Welcome to Randomeur!")
    output.note(1, settings['prefix'])
    print()
    output.option(1, "Flipeur")
    output.option(2, "Game Statistics")
    output.option(8, "Help")
    output.option(9, "Reset RND Statistics")
    output.option(0, "Home")

    choice = intake.prompt()
    choice = choiceCheck(choice)

    if choice == "1" or choice.casefold() in (f"flipeur", "coin flipeur", "coin"):
        clear()
        rnd.flipeur()

        apps['rnd']['heads']    += rnd.heads
        apps['rnd']['tails']    += rnd.tails
        apps['rnd']['flips']    += rnd.flips
        if rnd.heads == rnd.tails:
            apps['rnd']['ties'] += 1
        writeYAML()

        apps['rnd']['last-heads']       = rnd.heads
        apps['rnd']['last-tails']       = rnd.tails
        apps['rnd']['last-flips']       = rnd.flips
        writeYAML()

        apps['rnd']['last-winner']      = rnd.winner
        writeYAML()

        back()
    elif choice == "2" or choice.casefold() == "stats":
        clear()
        statsMenu()
        back()
    elif choice == "8" or choice.casefold() == "help":
        clear()
        helpRNDF()
        back()
    elif choice == "9" or choice.casefold() == "reset":
        clear()
        statsReset()
        back()
    elif choice == "0":
        clear()
        mainMenu()
    else:
        clear()
        lastCheck(choice)

    back(-2)

#==================================================================#

def rpsMenu():
    updateWindow(f"rps")

    def whosBest():

        wins = [apps['rps']['cpu']['wins'], apps['rps']['p1']['wins'], apps['rps']['p2']['wins']]
        name = [rps.cpu['name'], rps.p1['name'], rps.p2['name']]

        best = max(wins)
        bestIndex = wins.index(best)

        wins.remove(best)
        best2 = max(wins)

        if best == best2:
            return '—'

        #if len(set(wins)) < len(wins):
        #    return '—'

        return name[bestIndex]

    def statsMenu():
        print()
        output.stamp(f"RockPaperScissors Statistics:\n")
        print(f" {X0.YELLOW}-{C0.END} " + f"{rps.p1['name']} Wins        : {X0.GRAY}{apps['rps']['p1']['wins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"{rps.p1['name']} Last Choice : {X0.GRAY}{apps['rps']['p1']['last-choice']}{C0.END}")
        print()
        print(f" {X0.YELLOW}-{C0.END} " + f"{rps.p2['name']} Wins        : {X0.GRAY}{apps['rps']['p2']['wins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"{rps.p2['name']} Last Choice : {X0.GRAY}{apps['rps']['p2']['last-choice']}{C0.END}")
        print()
        print(f" {X0.YELLOW}-{C0.END} " + f"{rps.cpu['name']} Wins        : {X0.GRAY}{apps['rps']['cpu']['wins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"{rps.cpu['name']} Last Choice : {X0.GRAY}{apps['rps']['cpu']['last-choice']}{C0.END}")
        print()
        print(f" {X0.YELLOW}-{C0.END} " + f"Ties : {X0.GRAY}{apps['rps']['ties']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Best : {X0.GRAY}{whosBest()}{C0.END}")
        enterContinue()

    def statsReset():
        if confirm(output.notify(f"Are you sure?", Print= False)):
            resetRPS()
            clear()
            output.success(f"All done, good as new.")
            back()
        else:
            clear()
            output.error(f"Okay then.")
            back()

    print()
    output.stamp(f"Welcome to RockPaperScissors!")
    output.note(1, settings['prefix'])
    print()
    output.option(1, "Solo")
    output.option(2, "Duo")
    output.option(3, "Game Statistics")
    output.option(8, "Help")
    output.option(9, "Reset RPS Statistics")
    output.option(0, "Home")

    choice = intake.prompt()
    choice = choiceCheck(choice)

    if choice == "1" or choice.casefold() == "solo":
        rps.soloMode()

        pN = rps.pN
        p1 = rps.p1
        cpu = rps.cpu
        winner = rps.winner

        apps['rps']['p1']['last-choice']  = p1['input']
        apps['rps']['cpu']['last-choice'] = cpu['input']
        apps['rps']['last-winner']        = winner['name']
        writeYAML()

        if winner == p1:
            apps['rps']['p1']['wins'] += 1
        if winner == cpu:
            apps['rps']['cpu']['wins'] += 1
        if winner == pN:
            apps['rps']['ties'] += 1
        writeYAML()

        back()

    elif choice == "2" or choice.casefold() == "duo":
        rps.duoMode()

        pN = rps.pN
        p1 = rps.p1
        p2 = rps.p2
        winner = rps.winner

        apps['rps']['p1']['last-choice'] = p1['input']
        apps['rps']['p2']['last-choice'] = p2['input']
        apps['rps']['last-winner']       = winner['name']
        writeYAML()

        if winner == p1:
            apps['rps']['p1']['wins'] += 1
        if winner == p2:
            apps['rps']['p2']['wins'] += 1
        if winner == pN:
            apps['rps']['ties'] += 1
        writeYAML()

        back()

    elif choice == "3" or choice.casefold() == "stats":
        clear()
        statsMenu()
        back()
    elif choice == "8" or choice.casefold() == "help":
        clear()
        helpRPSF()
        back()
    elif choice == "9" or choice.casefold() == "reset":
        clear()
        statsReset()
        back()
    elif choice == "0":
        clear()
        mainMenu()
    else:
        clear()
        lastCheck(choice)

    back(-2)

#==================================================================#

def tttMenu():
    updateWindow(f"ttt")

    def tttGameMenu():
        global tttGameSubMenu
        tttGameSubMenu = tttGameMenu
        updateWindow("tttGameSub")

        print()
        output.stamp("Game Menu:")
        output.note(1, settings['prefix'])
        print()
        output.option(1, "Start Game")
        output.option(2, "Difficulty: " + X0.LETTUCE + apps['ttt']['diff'])
        output.option(0, "Back")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        result = None

        if choice == "1":
            clear()
            print()
            output.notify("Game mode...")
            output.note(1, settings['prefix'])
            print()
            output.option(1, "Solo")
            output.option(2, "Duo")
            output.option(0, "Back")
            choice = intake.prompt()
            choice = choiceCheck(choice)
            if choice == "1":
                result = ttt.soloMode(apps['ttt']['diff'])
                if not result:
                    back(-2)
            if choice == "2":
                result = ttt.duoMode()
                if not result:
                    back(-2)
            if choice == "0":
                clear()
                back()
            return result
        if choice == "2":
            clear()
            print()
            output.stamp(f"What do you want the difficulty to be? {X0.LETTUCE}(H,M,E)")
            output.note(1, settings['prefix'])
            output.note(f"Current is {X0.LETTUCE}{apps['ttt']['diff']}{C0.END}")
            print()
            allowed = "HME123"
            choice = intake.prompt()
            choice = choiceCheck(choice)
            if goThro(choice.upper(), allowed) and len(choice) == 1:
                if choice == "1": choice = "H"
                if choice == "2": choice = "M"
                if choice == "3": choice = "E"
                apps['ttt']['diff'] = choice.upper()
                writeYAML()
                clear()
                output.success("Changes saved.")
                back()
            else:
                clear()
                output.error("No, no, no. Only: Hard, Medium, Easy")
                back()
        if choice == "0":
            clear()
            back(-2)

    def statsMenu():
        print()
        output.stamp(f"TicTacToe Statistics:\n{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"X Wins     : {X0.GRAY}{apps['ttt']['x-wins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"O Wins     : {X0.GRAY}{apps['ttt']['o-wins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Ties       : {X0.GRAY}{apps['ttt']['ties']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last Winner: {X0.GRAY}{apps['ttt']['last-winner']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last Board :-\n")
        print(ttt.displayBoard(apps['ttt']['last-board'], True, left=f' {X0.YELLOW}-{C0.END} '))
        enterContinue()

    def statsReset():
        if confirm(output.notify(f"Are you sure?", Print= False)):
            resetTTT()
            clear()
            output.success(f"All done, good as new.")
            back()
        else:
            clear()
            output.error(f"Okay then.")
            back()

    print()
    output.stamp(f"Welcome to TicTacToe!")
    output.note(1, settings['prefix'])
    print()
    output.option(1, "Game Menu")
    output.option(2, "Game Statistics")
    output.option(8, "Help")
    output.option(9, "Reset TTT Statistics")
    output.option(0, "Home")

    choice = intake.prompt()
    choice = choiceCheck(choice)

    if choice == "1" or choice.casefold() == "start":
        clear()
        result = tttGameMenu()

        if type(result) == type(["Oh", "hey there", "cutie!"]): 
            winner = result[0]
            board = result[1]

            apps['ttt']['last-winner'] = winner['name']
            apps['ttt']['last-board'] = board

            if winner == ttt.s.x:
                apps['ttt']['x-wins'] = int(apps['ttt']['x-wins']) + 1
            if winner == ttt.s.o:
                apps['ttt']['o-wins'] = int(apps['ttt']['o-wins']) + 1
            if winner == ttt.tied:
                apps['ttt']['ties'] = int(apps['ttt']['ties']) + 1
            writeYAML()

        back()

    elif choice == "2" or choice.casefold() == "stats":
        clear()
        statsMenu()
        back()
    elif choice == "8" or choice.casefold() == "help":
        clear()
        helpTTTF()
        back()
    elif choice == "9" or choice.casefold() == "reset":
        clear()
        statsReset()
        back()
    elif choice == "0":
        clear()
        mainMenu()
    else:
        clear()
        lastCheck(choice)

    back(-2)

#==================================================================#

def mspMenu():
    global mspBD
    updateWindow(f"msp")

    def mspConfMenu():
        global mspConfSubMenu
        mspConfSubMenu = mspConfMenu
        updateWindow("mspConfSub")

        print()
        output.stamp("Minesweeper Config:")
        output.note(1, settings['prefix'])
        print()
        output.option(1, "Map Size: " + X0.LETTUCE + str(apps['msp']['dim']) + C0.END)
        output.option(2, "Bomb Count: " + X0.LETTUCE + str(apps['msp']['bombC']) + C0.END)
        output.option(0, "Back")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        if choice == "1":
            clear()
            print()
            output.stamp("What do you want the map size to be?")
            output.note(1, settings['prefix'])
            output.note(f"Map size ranges from {X0.YELLOW}1:99{C0.END}")
            output.note(f"I don't recommend anything above 25 for your machine's health, also I do not recommend anything above 10 for the looks of it.")
            output.note(f"Current is {X0.LETTUCE}{apps['msp']['dim']}{C0.END}")
            print()

            choice = intake.prompt()
            choice = choiceCheck(choice)

            allowed = "0123456789"
            if goThro(choice, allowed):
                choice = int(choice)
                if 99 >= choice > 0:
                    apps['msp']['dim'] = choice
                    writeYAML()
                    clear()
                    output.success("Changes saved.")
                    back()

        if choice == "2":
            clear()
            print()
            output.stamp("How many bombs do you want there to be?")
            output.note(1, settings['prefix'])
            output.note(f"Bombs count ranges from {X0.YELLOW}1:{apps['msp']['dim']**2}{X0.END}")
            output.note(f"Current is {X0.LETTUCE}{apps['msp']['bombC']}{C0.END}")
            print()

            choice = intake.prompt()
            choice = choiceCheck(choice)

            allowed = "0123456789"
            if goThro(choice, allowed):
                choice = int(choice)
                if (apps['msp']['dim']**2) >= choice > 0:
                    apps['msp']['bombC'] = choice
                    writeYAML()
                    clear()
                    output.success("Changes saved.")
                    back()
        if choice == "0":
            clear()
            back(-2)

        clear()
        lastCheck(choice)

    def statsMenu():
        print()
        output.stamp(f"Minesweeper Statistics:\n")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total Wins :     {X0.GRAY}{apps['msp']['wins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total Loses:     {X0.GRAY}{apps['msp']['defeats']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total Dug Spots: {X0.GRAY}{apps['msp']['spots-dug']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last Map:-")
        #print(f" {x.YELLOW}-{c.END} " + f": {x.GRAY}{apps['msp']['']}{c.END}")

        mspBD.print(True)

        enterContinue()

    def statsReset():
        if confirm(output.notify(f"Are you sure?", Print= False)):
            resetMSP()
            clear()
            output.success(f"All done, good as new.")
            back()
        else:
            clear()
            output.error(f"Okay then.")
            back()

    print()
    output.stamp(f"Welcome to Minesweeper!")
    output.note(1, settings['prefix'])
    print()
    output.option(1, "Start a Game")
    output.option(2, "Config")
    output.option(3, "Game Statistics")
    output.option(8, "Help")
    output.option(9, "Reset MSP Statistics & Config")
    output.option(0, "Home")

    choice = intake.prompt()
    choice = choiceCheck(choice)

    if choice == "1":
        clear()
        dim   = apps['msp']['dim']
        bombC = apps['msp']['bombC']
        msp.startGame( SIZE = dim, BOMBS = bombC )

        if msp.gameWon:
            apps['msp']['wins']  += 1
        else:
            apps['msp']['defeats'] += 1

        apps['msp']['spots-dug'] += len(msp.BD.playerDug)
        mspBD = msp.BD

        writeYAML()
        writePICKLE()
        back()

    elif choice == "2" or choice.casefold() == "config":
        clear()
        mspConfMenu()
        back(-2)
    elif choice == "3" or choice.casefold() == "stats":
        clear()
        statsMenu()
        back()
    elif choice == "8" or choice.casefold() == "help":
        clear()
        helpMSPF()
        back()
    elif choice == "9" or choice.casefold() == "reset":
        clear()
        statsReset()
        back()
    elif choice == "0":
        clear()
        mainMenu()
    else:
        clear()
        lastCheck(choice)

    back(-2)

#==================================================================#

def bjkMenu():
    updateWindow(f"bjk")

    def bjkConfMenu():
        global bjkConfSubMenu
        bjkConfSubMenu = bjkConfMenu
        updateWindow("bjkConfSub")

        print()
        output.stamp("BlackJack Config:")
        output.note(1, settings['prefix'])
        print()
        output.option(1, "Hit on Soft 17: " + (f"{X0.LETTUCE}Yes" if apps['bjk']['soft-17'] else f"{X0.RED}No") + C0.END)
        output.option(0, "Back")

        choice = intake.prompt()
        choice = choiceCheck(choice)
        
        if choice == "1":
            clear()
            output.stamp("Hit on Soft 17? " + f"{X0.GRAY}({X0.LETTUCE}Y{X0.GRAY},{X0.RED}N{X0.GRAY})")
            output.note(1, settings['prefix'])
            output.note(f"To explain, this option is to either make the dealer hit on 17 or not.")
            output.note(f"")
            output.note(f"Current is {(f'{X0.LETTUCE}Yes' if apps['bjk']['soft-17'] else f'{X0.RED}No')}")

            choice = intake.prompt()
            choice = choiceCheck(choice)

            if goThro(choice, "YNyn12"):
                if choice.upper() in ("Y", "1"):
                    apps['bjk']['soft-17'] = True
                if choice.upper() in ("N", "2"):
                    apps['bjk']['soft-17'] = False
                writeYAML()
                clear()
                output.success("Changes saved.")
                back()

        if choice == "0":
            clear()
            back(-2)

        clear()
        lastCheck(choice)

    def statsReset():
        if confirm(output.notify(f"Are you sure?", Print= False)):
            resetBJK()
            clear()
            output.success(f"All done, good as new.")
            back()
        else:
            clear()
            output.error(f"Okay then.")
            back()

    print()
    output.stamp("Welcome to BlackJack!")
    output.note(1, settings['prefix'])
    output.note(f"Current Balance is {X0.LETTUCE}{apps['bjk']['balance']}C")
    print()
    output.option(1, "Start a Game")
    output.option(2, "la Banque")
    output.option(3, "Config")
    output.option(8, "Help")
    output.option(9, "Reset BJK Statistics & Config")
    output.option(0, "Home")

    choice = intake.prompt()
    choice = choiceCheck(choice)

    if choice == "1":

        clear()
        result    = bjk.startGame(apps['bjk']['balance'], 1, apps['bjk']['soft-17'])

        apps['bjk']['balance']  = result[0]
        apps['bjk']['last-bet'] = result[1]

        writeYAML()

        back()

    elif choice == "2":

        available = apps['bjk']['reward'] != today
        clear()

        print()
        output.stamp(f"Bienvenue à la Banque de {X0.LETTUCE}SPAIME²{X0.VIOLET}!")
        output.note(1, settings['prefix'])
        output.note("Reward " + ((f"{X0.LETTUCE}available") if available else (f"{X0.RED}not available")) + f"{X0.GRAY}.")
        print()
        output.option(1, (C0.STRIKE if not available else "") + "Claim Daily")
        output.option(2, "Debt")
        output.option(0, "Back")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        if choice == "1" and available:
            clear() 

            apps['bjk']['reward'] = today
            luck = random.randint(1,10)
            h1,h2,h3,h4 = ("",)*4

            if 1 <= luck <= 4:
                reward = 500
                h1 = X0.GOLDBG + X0.BLACK
            if 5 <= luck <= 7:
                reward = 1000
                h2 = X0.GOLDBG + X0.BLACK
            if 8 <= luck <= 9:
                reward = 2000
                h3 = X0.GOLDBG + X0.BLACK
            if 10 <= luck <= 10:
                reward = 5000
                h4 = X0.GOLDBG + X0.BLACK

            output.notify("Hey, hey there, High-Roller!")
            print(
                f"> {h1}{X0.GRAY}[{X0.LETTUCE}500C{X0.GRAY}]{C0.END} "
                + f"{h2}{X0.GRAY}[{X0.LETTUCE}1000C{X0.GRAY}]{C0.END} "
                + f"{h3}{X0.GRAY}[{X0.LETTUCE}2000C{X0.GRAY}]{C0.END} "
                + f"{h4}{X0.GRAY}[{X0.LETTUCE}5000C{X0.GRAY}]{C0.END} <")
            if available:
                apps['bjk']['balance'] += reward
            writeYAML()
            enterContinue()
        elif choice == "1":
            clear()
            output.error("That's greedy.")
            back()
        elif choice == "2":
            clear()
            output.notify("Coming soon!")
            back()
        else:
            clear()
            output.error("Invalid input.")
            back()
        clear()
        back()


    elif choice == "3":
        clear()
        bjkConfMenu()
        back(-2)
    elif choice == "8":
        clear()
        helpBJKF()
        back()
    elif choice == "9":
        clear()
        statsReset()
        back()
    elif choice == "0":
        clear()
        mainMenu()
    else:
        clear()
        lastCheck(choice)

    mainMenu()

#==================================================================#

def sdkMenu():
    global sdkBD
    updateWindow(f"sdk")

    def sdkConfMenu():
        global sdkConfSubMenu
        sdkConfSubMenu = sdkConfMenu
        updateWindow("sdkConfSub")

        print()
        output.stamp("Sudoku Config:")
        output.note(1, settings['prefix'])
        print()
        output.option(1, f"Empty Spots: {X0.LETTUCE}{apps['sdk']['empty']}{C0.END}")
        output.option(0, f"Back")

        choice = intake.prompt()
        choice = choiceCheck(choice)
        
        if choice == "1":
            clear()
            output.stamp("How many empty spots do you want?!")
            output.note(1, settings['prefix'])
            output.note(f"Current is {X0.LETTUCE}{apps['sdk']['empty']}")

            choice = intake.prompt()
            choice = choiceCheck(choice)

            if goThro(choice, "0123456789"):
                choice = int(choice)

                if 81 >= choice > 0:
                    apps['sdk']['empty'] = choice

                    writeYAML()
                    clear()
                    output.success("Changes saved.")
                    back()
                else:
                    clear()
                    output.error("Number needs to be between 0 and 81, 0 not included.")
                    back()

        if choice == "0":
            clear()
            back(-2)

        clear()
        lastCheck(choice)

    def statsMenu():
        print()
        output.stamp(f"Sudoku Statistics:\n")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total Wins :     {X0.GRAY}{apps['sdk']['wins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total Validations: {X0.GRAY}{apps['sdk']['validated']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last Puzzle:-")

        sdkBD.print(D=False)

        enterContinue()

    def statsReset():
        if confirm(output.notify(f"Are you sure?", Print= False)):
            resetSDK()
            clear()
            output.success(f"All done, good as new.")
            back()
        else:
            clear()
            output.error(f"Okay then.")
            back()

    print()
    output.stamp("Welcome to Sudoku!")
    output.note(1, settings['prefix'])
    print()
    output.option(1, "Continue")
    output.option(2, "New Game")
    output.option(3, "Config")
    output.option(4, "Game Statistics")
    output.option(8, "Help")
    output.option(9, "Reset SDK Statistics & Config")
    output.option(0, "Home")

    choice = intake.prompt()
    choice = choiceCheck(choice)

    if   choice == "1":
        clear()
        sdk.startGame(apps['sdk']['empty'], settings['prefix'], sdkBD)

        sdkBD                    = sdk.sudoku
        apps['sdk']['wins']     += 1 if sdk.gameWon else 0
        apps['sdk']['validated'] = sdk.sudoku.timesVal

        writeYAML()
        writePICKLE()
        back()
    elif choice == "2":
        clear()
        sdk.startGame(apps['sdk']['empty'], settings['prefix'])

        sdkBD                    = sdk.sudoku
        apps['sdk']['wins']     += 1 if sdk.gameWon else 0
        apps['sdk']['validated'] = sdk.sudoku.timesVal

        writeYAML()
        writePICKLE()
        back()
    elif choice == "3":
        clear()
        sdkConfMenu()
        back()
    elif choice == "4":
        clear()
        statsMenu()
        back()
    elif choice == "8":
        clear()
        helpSDKF()
        back()
    elif choice == "9":
        clear()
        statsReset()
        back()
    elif choice == "0":
        clear()
        mainMenu()
    else:
        clear()
        lastCheck(choice)

    mainMenu()


#==================================================================#

def bfiMenu():
    updateWindow(f"bfi")

    output.stamp("Welcome to BrainFuck Interpreter!")
    output.note(1, settings['prefix'])
    print()
    output.option(1, "Run a File")
    output.option(2, "View Files")
    output.option(3, "Compile")
    output.option(0, "Home")

    choice = intake.prompt()
    choice = choiceCheck(choice)

    if   choice == "1":
        clear()
        bfi.startApp('R')

    elif choice == "2":
        clear()
        bfi.startApp('D')

    elif choice == "3":
        clear()
        bfi.startApp('C')

    elif choice == "0":
        clear()
        mainMenu()

    else:
        clear()
        lastCheck(choice)

    back()

#==================================================================#

def optionsMenu():
    updateWindow(f"options")

    def nameChange(name):
        user['name'] = str(name)
        try:
            writeYAML()
        except:
            clear()
            output.error(f"Something went wrong.")
        else:
            writeYAML()
            clear()
            output.success(f"Changes saved.")

    def sexChange(sex:str):

        if sex.capitalize() in ("M", "F", "N"):

            if sex.upper() == "M":
                sex = "Male"
            if sex.upper() == "F":
                sex = "Female"
            if sex.upper() == "N":
                sex = "Non-Binary"

            user['sex'] = sex

            try:
                writeYAML()
            except:
                clear()
                output.error(f"Something went wrong.")
            else:
                writeYAML()
                clear()
                output.success(f"Changes saved.")

        elif sex.upper() == "MF":
            clear()
            output.warn("Are you calling me a mf...?")

        else:
            clear()
            output.error(f"What gender is that?! Available Options: male, female, non-binary")

    def ageChange(age):
        age_old = user['age']
        try:
            user['age'] = int(age)
        except:
            clear()
            output.error(f"Please input numbers only.")
        else:
            if (user['age'] >= 100 or user['age'] < 0) and not (isAdmin()):
                clear()
                output.error(f"How tf can you be {user['age']} years-old?")
                output.error(f"I'll return it to {age_old}.")
                user['age'] = age_old
                return
            try:
                writeYAML()
            except:
                clear()
                output.error(f"Something went wrong.")
            else:
                writeYAML()
                clear()
                if user['age'] == 69:
                    output.success(f"Nice.")
                else:
                    output.success(f"Changes saved.")

    def prefix_change(thing):
        clear()
        settings['prefix'] = thing
        writeYAML()

    print()
    output.stamp(f"Options:")
    output.note(1, settings['prefix'])
    print()
    output.option(1, f"Name: {X0.GREEN}{user['name'] if user['name'] != '' else 'N/A'}")
    output.option(2, f"Gender: {X0.GREEN}{user['sex'] if user['sex'] != None else 'N/A'}")
    output.option(3, f"Age: {X0.GREEN}{user['age']}")
    output.option(4, f"Prefix: {X0.GREEN}{settings['prefix']}")
    output.option(8, f"Rest Games' Stats")
    output.option(9, f"Rest Application")
    output.option(0, f"Home")

    choice = intake.prompt()
    choice = choiceCheck(choice)

    if choice == "1" or choice.casefold() == "name":

        clear()
        print()
        output.stamp(f"What do you wanna be called?")
        output.note(1, settings['prefix'])
        output.note(f"Current is {X0.GREEN}{user['name'] if user['name'] != '' else 'N/A'}")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        nameChange(choice)

        back()

    elif choice == "3" or choice.casefold() == "age":

        clear()
        print()
        output.stamp(f"How old are you?")
        output.note(1, settings['prefix'])
        output.note(f"Current is {X0.GREEN}{user['age']}")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        ageChange(choice)

        back()
    elif choice == "2" or choice.casefold() == "gender":

        clear()
        print()
        output.stamp(f"Cation, Anion or Zwitterion? {X0.LETTUCE}(M,F,N)")
        output.note(1, settings['prefix'])
        output.note(f"Current is {X0.GREEN}{user['sex'] if user['sex'] != None else 'N/A'}")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        sexChange(choice)

        back()
    elif choice == "4" or choice.casefold() == "prefix":

        clear()
        print()
        output.stamp(f"Set prefix to what?")
        output.note(1, settings['prefix'])
        output.note(f"Current is {X0.GREEN}{settings['prefix']}")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        prefix_change(choice)

        back()
    elif choice == "8" or choice.casefold() == "reset stats":

        clear()
        output.notify(f"Continuing would mean you want to reset statistics to default.")
        if confirm(output.notify(f"Are you sure?", Print=False)):
            print()
            output.notify(f"Please type {X0.GRAY}{C0.ITALIC}\"{X0.LETTUCE}{settings['prefix']}reset{X0.GRAY}\"{C0.END}{X0.GRAY} to further confirm.")

            choice = intake.prompt()
            choice = choiceCheck(choice)

            if choice == f"{settings['prefix']}reset":
                resetYAML(apps)
                clear()
                output.success(f"All done, good as new.")
                back()
            else:
                clear()
                output.error(f"I'll take that as a \"no\".")
                back()
        else:
            clear()
            output.error(f"Ready when you're are.")
            back()

    elif choice == "9" or choice.casefold() == "reset all" or choice.casefold() == "reset app" or choice.casefold() == "reset application" :

        clear()
        output.notify(f"Continuing would mean you want to reset statistics to default.")
        if confirm(output.notify(f"Are you sure?", Print=False)):
            print()
            output.notify(f"Please type {X0.GRAY}{C0.ITALIC}\"{X0.LETTUCE}{settings['prefix']}reset{X0.GRAY}\"{C0.END}{X0.GRAY} to further confirm.")

            choice = intake.prompt()
            choice = choiceCheck(choice)

            if choice == f"{settings['prefix']}reset":
                resetYAML()
                resetPICKLE()
                clear()
                output.success(f"All done, good as new. {C0.END}")
                back()
            else:
                clear()
                output.error(f"I'll take that as a \"no\".")
                back()
        else:
            clear()
            output.error(f"Ready when you're are.")
            back()
    elif choice == "0":
        clear()
        mainMenu()
    else:
        clear()
        lastCheck(choice)

    back(-2)

#==================================================================#






####################################################################
##                                                                ##
##                              Mics.                             ##
##                                                                ##
####################################################################


def helpF():
    """The cmd & plh help menu."""

    print()
    output.stamp(f"Commands:")
    # The available SPAIME commands.
    print(f" {X0.YELLOW}-{C0.END} {settings['prefix']}" + f"help [┬]   : {X0.GRAY}Shows this menu.{C0.END}")
    print(                                          f"          ├math: {X0.GRAY}Shows help about Math & Logic.{C0.END}")
    print(                                          f"          ├rnd : {X0.GRAY}Shows help about Randomeur.{C0.END}")
    print(                                          f"          ├rps : {X0.GRAY}Shows help about RockPaperScissors.{C0.END}")
    print(                                          f"          ├ttt : {X0.GRAY}Shows help about TicTacToe.{C0.END}")
    print(                                          f"          ├msp : {X0.GRAY}Shows help about Minesweeper.{C0.END}")
    print(                                          f"          └bjk : {X0.GRAY}Shows help about BlackJack.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {settings['prefix']}" + f"back:        {X0.GRAY}Returns you a page back.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {settings['prefix']}" + f"home:        {X0.GRAY}Returns you to home page.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {settings['prefix']}" + f"refr:        {X0.GRAY}Refreshes current page.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {settings['prefix']}" + f"exit:        {X0.GRAY}To safely exit the app.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {settings['prefix']}" + f"dev1:        {X0.GRAY}Enters eval() mode. {X0.RED}{C0.DIM}(dev-only){C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {settings['prefix']}" + f"dev2:        {X0.GRAY}Enters exec() mode. {X0.RED}{C0.DIM}(dev-only){C0.END}")
    print("\n")
    output.stamp(f"Placeholders:")
    # The available placeholders.
               # The syntax ones.
    print(f" {X0.YELLOW}-{C0.END}" + " {nl}: " + f"           {X0.GRAY}Makes a lovely line separator, not useful.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {br}: " + f"           {X0.GRAY}Makes a new line, useful in repeat, I guess.{C0.END}")
    print(f"") # The user & settings ones.
    print(f" {X0.YELLOW}-{C0.END}" + " {name}: " + f"         {X0.GRAY}Returns your name.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {age}: " + f"          {X0.GRAY}Returns your age.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {prefix}: " + f"       {X0.GRAY}Returns set prefix{C0.END}")
    print(f"") # The math & physics ones.
    print(f" {X0.YELLOW}-{C0.END}" + " {e}: " + f"            {X0.GRAY}Returns Euler's number's value.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {g}: " + f"            {X0.GRAY}Returns gravitational acceleration constant's value.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {pi}: " + f"           {X0.GRAY}Returns pi's value.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {tau}: " + f"          {X0.GRAY}Returns tau's value.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {phi}: " + f"          {X0.GRAY}Returns the golden ratio's value.{C0.END}")
    print(f"") # The Randomeur ones.
    print(f" {X0.YELLOW}-{C0.END}" + " {heads}: " + f"        {X0.GRAY}Returns the total amount of {rnd.headsStyle}{X0.GRAY}.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {tails}: " + f"        {X0.GRAY}Returns the total amount of {rnd.tailsStyle}{X0.GRAY}.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {rndTies}: " + f"      {X0.GRAY}Returns the total amount of RND {rnd.tieStyle}{X0.RED}s{X0.GRAY}.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {flips}: " + f"        {X0.GRAY}Returns the total amount of RND {rnd.flipsStyle}{X0.GRAY}.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {lastHeads}: " + f"    {X0.GRAY}Returns the last {rnd.headsStyle}{X0.GRAY} count.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {lastTails}: " + f"    {X0.GRAY}Returns the last {rnd.tailsStyle}{X0.GRAY} count.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {lastFlips}: " + f"    {X0.GRAY}Returns the last {rnd.flipsStyle}{X0.GRAY} count.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {lastRNDWinner}: " + f"{X0.GRAY}Returns the last RND winner.{C0.END}")
    print(f"") # The RockPaperScissors ones.
    print(f" {X0.YELLOW}-{C0.END}" + " {p1Last}: " + f"       {X0.GRAY}Returns {rps.p1['name']}{X0.GRAY} last move.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {p2Last}: " + f"       {X0.GRAY}Returns {rps.p2['name']}{X0.GRAY} last move.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {cpuLast}: " + f"      {X0.GRAY}Returns {rps.cpu['name']}{X0.GRAY} last move.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {p1Wins}: " + f"       {X0.GRAY}Returns how many times {rps.p1['name']}{X0.GRAY} won.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {p2Wins}: " + f"       {X0.GRAY}Returns how many times {rps.p2['name']}{X0.GRAY} won.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {cpuWins}: " + f"      {X0.GRAY}Returns how many times {rps.cpu['name']}{X0.GRAY} won.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {rpsTies}: " + f"      {X0.GRAY}Returns how many times RPS ties happened.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {lastRPSWinner}: " + f"{X0.GRAY}Returns the last RPS winner.{C0.END}")
    print(f"") # The TicTacToe ones.
    print(f" {X0.YELLOW}-{C0.END}" + " {lastTTTWinner}: " + f"{X0.GRAY}Returns the last TTT winner.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {lastTTTBoard}: " + f" {X0.GRAY}Returns the last TTT board.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {xWins}: " + f"        {X0.GRAY}Returns how many times x won.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {oWins}: " + f"        {X0.GRAY}Returns how many times o won.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {tttTies}: " + f"      {X0.GRAY}Returns how many TTT ties happened.{C0.END}")
    print(f"") # The Minesweeper ones.
    print(f" {X0.YELLOW}-{C0.END}" + " {mspWins}: " + f"      {X0.GRAY}Returns how many times you won at MSP.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {mspDefeats}: " + f"   {X0.GRAY}Returns how many times you lost at MSP.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {mspDug}: " + f"       {X0.GRAY}Returns how many times you dug manually at MSP.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {mspBombs}: " + f"     {X0.GRAY}Returns how many bombs are in MSP config.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END}" + " {mspSize}: " + f"      {X0.GRAY}Returns how big the map is in MSP config.{C0.END}")

    enterContinue()

#==================================================================#

def helpMathF():

    print()
    output.stamp("Math & Logic Help:")

    output.note(f"You can use basic math and logic gates.", sign="D")
    output.note(f'Allowed Input: "{X0.LETTUCE}0123456789+-*×x/\\÷^.,()%=TF!&| {C0.END}{X0.GRAY}".', sign="D")
    output.note(f"T  {X0.LETTUCE}->{X0.GRAY} True", sign="D")
    output.note(f"F  {X0.LETTUCE}->{X0.GRAY} False", sign="D")
    output.note(f"!  {X0.LETTUCE}->{X0.GRAY} not", sign="D")
    output.note(f"&  {X0.LETTUCE}->{X0.GRAY} and", sign="D")
    output.note(f"|  {X0.LETTUCE}->{X0.GRAY} or", sign="D")
    output.note(f"== {X0.LETTUCE}->{X0.GRAY} equal-to", sign="D")
    output.note(f"!= {X0.LETTUCE}->{X0.GRAY} not-equal-to", sign="D")

    enterContinue()

#==================================================================#

def helpRNDF():

    print()
    output.stamp("Randomeur Help:")

    print()
    output.notify("Flipeur:")

    output.note(f"Flip a coin for [{X0.LETTUCE}x-amount{X0.GRAY}] of times.", sign="D")
    output.note(f"[{X0.LETTUCE}x-amount{X0.GRAY}] must be between {X0.LETTUCE}1:10000.", sign="D")
    output.note(f"That is so you don't smell a grilled CPU core.", sign="D")
    output.note(f"Check on the statistics to see some cool figures.", sign="D")

    enterContinue()

#==================================================================#

def helpRPSF():
    print()
    output.stamp("RockPaperScissors Help:")
    output.note(f"There're two main modes:", sign="D")
    output.note(f"You choose rock, paper or scissors and the CPU randomizes a choice.", sign=f"{X0.YELLOW}Solo:")
    output.note(f"You choose rock, paper or scissors and call a friend to choose too.", sign=f"{X0.YELLOW}Duo :")
    output.note(f"Check on the statistics to see some cool figures.", sign="D")

    enterContinue()

#==================================================================#

def helpTTTF():
    print()
    output.stamp("TicTacToe Help:")
    output.note(f"First, choose whether to start with {ttt.s.x}{X0.GRAY} or {ttt.s.o}{X0.GRAY}.", sign="D")
    output.note(f"Next, just type the position number you want to play at.", sign="D")
    output.note(f"Check on the statistics to see some cool figures.", sign="D")

    enterContinue()

#==================================================================#

def helpMSPF():
    print()
    output.stamp("Minesweeper Help:")
    output.note(f"{msp.bombS} {X0.GRAY}Boom!!", sign="D")
    output.note(f"Let's start by talking about the Config page.", sign="D")
    output.note(f"There you can choose the map size and the amount of bombs.", sign="D")
    output.note(f"To dig a spot just type {C0.ITALIC}'[{X0.LETTUCE}x,y{X0.GRAY}]'{C0.END}{X0.GRAY} of that spot.", sign="D")
    output.note(f"To flag a spot just type {C0.ITALIC}'[{X0.LETTUCE}x,y{X0.GRAY}]{msp.flagS}'{C0.END}{X0.GRAY} of that spot.", sign="D")
    output.note(f"Any brackets like {X0.LETTUCE}(){X0.GRAY}, {X0.LETTUCE}[]{X0.GRAY} or {X0.LETTUCE}{bricks}{X0.GRAY}, and spaces are ignored.", sign="D")
    output.note(f"{msp.emptyS} {X0.LETTUCE}->{X0.GRAY} Not Dug", sign="D")
    output.note(f"{msp.nS[ random.randint(0,len(msp.nS)) -1 ]} {X0.LETTUCE}->{X0.GRAY} Dug", sign="D")
    output.note(f"{msp.flagS} {X0.LETTUCE}->{X0.GRAY} Flagged", sign="D")
    output.note(f"{msp.bombS} {X0.LETTUCE}->{X0.GRAY} Bomb", sign="D")
    output.note(f"Check on the statistics to see some cool figures.", sign="D")

    enterContinue()

#==================================================================#

def helpBJKF():
    print()
    output.stamp("BlackJack Help:")
    output.note(f"Let's start by talking about the Config page.", sign="D")
    output.note(f"There you can choose whether {X0.LETTUCE}Hit-on-Soft-17{X0.GRAY} is applied or not.", sign="D")
    output.note(f"The game control menu is self-explanatory so I won't get into it.", sign="D")
    output.note(f"But an additional tip: You don't have to use the first letter, you can type its place number.", sign="D")
    output.note(f"Cards look like: {bjk.PROTO[random.randint(0,(len(bjk.PROTO)-1))]['s']}", sign="D")
    output.note(f"  ({X0.LETTUCE}The Card Value{X0.GRAY})┘│", sign="D")
    output.note(f"  ({X0.LETTUCE}The Card Suits{X0.GRAY})─┘", sign="D")
    enterContinue()

#==================================================================#

def helpSDKF():
    thing = "{x-pos,y-pos,number}"
    print()
    output.stamp("Sudoku Help:")
    output.note(f"Try to complete the {X0.LETTUCE}1:9{X0.GRAY} combination of number.", sign="D")
    output.note(f"Do that, vertically, horizontally and in the subsquares/subregions.", sign="D")
    output.note(f"Fill a spot by typing: {X0.LETTUCE}{thing}{X0.GRAY}. Spaces and brackets are ignored.", sign="D")
    enterContinue()

#==================================================================#

def infoF():
    """App and author info and shit you know."""

    # Reading the logo.txt file and separating it into its pieces.
    with open('./res/extras/logo.txt', 'r') as file:
        logo = file.read().split(f"-sex-is-cool-")
        logo_art = logo[0]
        logo_text = logo[1]
        logo_motto = logo[2]

    clear()

    # ASCII art for the logo, that shows on first launch.
    print( ""
        + X0.LETTUCE + logo_art + C0.END
        + X0.VIOLET + logo_text + C0.END
        + C0.DIM
        + X0.GRAY + logo_motto + C0.END
        )

    # Your usual yadda yadda.
    print()
    output.stamp(f"SPAIME²")
    output.option(f"Version", f"x.x.x{C0.END}")
    output.option(f"Author", f" Fastre{C0.END}")
    output.option(f"Github", f" {C0.URL}{C0.ITALIC}https://github.com/IamFastre{C0.END}")
    output.option(f"Discord", f"{C0.URL}{C0.ITALIC}https://discord.gg/kkzmxkG{C0.END}")
    output.option(f"Note", f"   There was never a SPAIME¹{C0.END}")
    choice = enterContinue()

    # An easter egg!
    if choice.casefold() in admins:
        output.success(f"Yes, {X0.RED}♥{X0.GRAY}.{C0.END}")
    back()

#==================================================================#

def refreshF():
    """Practically does nothing, maybe clears notifications."""

    # It's just to clear notifications or print faults.
    clear()
    output.notify(f"Refreshing!")
    sleep(0.5)
    clear()
    back()

#==================================================================#

def exitF():
    """Delete annoying cache files and turn the app off."""

    print(f"{X0.YELLOW}>>{X0.GRAY} Okie!{C0.END}")
    sleep(0.5)
    clear()

    # Telling you sweet goodbyes.
    if user['name'] == '':
        output.notify(f"Bye-bye{X0.VIOLET}!")
    else:
        output.notify(f"Bye-bye, {X0.GREEN}{user['name']}{X0.VIOLET}!")

    # Deleting pycache, it makes the app run faster but screw it, am I right?
    delCache()
    enterContinue()

    # raising SystemExit without parsing errors.
    sys.exit(0)

#==================================================================#






####################################################################
##                                                                ##
##                          Running App.                          ##
##                                                                ##
####################################################################

if __name__ == "__main__":

    clear()

    if settings['first-time']:
        settings['first-time'] = False
        writeYAML()
        infoF()

    mainMenu()
    clear()

#==================================================================#
