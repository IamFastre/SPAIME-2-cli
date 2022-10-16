####################################################################
##                                                                ##
##    Importing important files, modules, packages and so on.     ##
##                                                                ##
####################################################################

import os, sys, random, shutil, subprocess, time, pickle

# Importing the other py files.
from res.colors import *
from res.codes import *
from res.libs import *
from time import *

#==================================================================#

# Importing the applets
import apps.ttt as ttt
import apps.rps as rps
import apps.rnd as rnd
import apps.msp as msp

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
        user = yaml.safe_load(USER)

    with open('./data/apps.yml', 'rb') as APPS:
        apps = yaml.safe_load(APPS)
    
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
    
    global settings
    global user
    global apps
    global YAMLS
    
    if YAML != None:
        i = YAMLS.index(YAML)
        
        if i == 0:
            shutil.copy('./data/.old/settings.yml', './data/')
        if i == 1:
            shutil.copy('./data/.old/user.yml', './data/')
        if i == 2:
            shutil.copy('./data/.old/apps.yml', './data/')
    else:
        for file in glob.glob('./data/.old/*.yml'):
            shutil.copy(file, './data/')

    readYAML()
            
#==================================================================#

def resetTTT():
    global apps
    apps['ttt'] = {'last-board': '—————————', 'last-winner': '—', 'x-wins': 0, 'o-wins': 0, 'ties': 0, 'diff': 'M'}
    writeYAML()

#==================================================================#

def resetRPS():
    global apps
    apps['rps'] = {'p1': {'wins': 0, 'last-choice': '—'}, 'p2': {'wins': 0, 'last-choice': '—'}, 'cpu': {'wins': 0, 'last-choice': '—'}, 'ties': 0}
    writeYAML()

#==================================================================#

def resetRND():
    global apps
    apps['rnd'] = {'ties': 0, 'heads': 0, 'tails': 0, 'flips': 0, 'last-heads': 0, 'last-tails': 0, 'last-flips': 0, 'last-winner': '—'}
    writeYAML()

#==================================================================#

def resetMSP():
    global apps
    apps['msp'] = {'wins': 0, 'defeats': 0, 'spots-dug': 0, 'bombC': 10, 'dim': 10}
    resetPICKLE(mspBD)
    writeYAML()

#==================================================================#

def readPICKLE():
    global mspBD
    global PICKLES

    with open('./data/mspBD.pkl', 'rb') as MSPBD:
        mspBD = pickle.load(MSPBD)
        
    PICKLES = (mspBD,)

#==================================================================#

def writePICKLE():
    global mspBD
    global PICKLES

    with open('./data/mspBD.pkl', 'wb') as MSPBD:
        pickle.dump(mspBD, MSPBD)
    
    readPICKLE()

#==================================================================#

def resetPICKLE(PICKLE = None):
    global mspBD
    global PICKLES
    
    if PICKLE != None:
        i = PICKLES.index(PICKLE)
        
        if i == 0:
            shutil.copy('./data/.old/mspBD.pkl', './data/')
    else:
        for file in glob.glob('./data/.old/*.pkl'):
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
admins = (f"fastre", "neria", "mahmoud")
passes = (576957, None)

commands = [
    settings['prefix'] + "help",
    settings['prefix'] + "home",
    settings['prefix'] + "exit",
    settings['prefix'] + "dev1",
    settings['prefix'] + "dev2",
    settings['prefix'] + "reset",
    ]

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

#==================================================================#

def isAdmin():
    return (user['name'].casefold() in admins and user['age'] in passes and user['sex'] == "Male")

#==================================================================#

def isCommand(thing):
    commands = [
        settings['prefix'] + "help",
        settings['prefix'] + "help math",
        settings['prefix'] + "help rnd",
        settings['prefix'] + "help rps",
        settings['prefix'] + "help ttt",
        settings['prefix'] + "help msp",

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
                print(f"\n{x.YELLOW}>> {x.VIOLETBG}{c.WHITE}{decoded.n69}{c.END}")
            else:
                print(f"\n{x.YELLOW}>>{x.GREEN} {user['name']}{c.END}, {x.VIOLETBG}{c.WHITE}{decoded.n69}{c.END}")
        else:
            if user['name'] == '':
                print(f"\n{x.YELLOW}>> {x.VIOLETBG}{c.WHITE}{decoded.n70}{c.END}")
            else:
                print(f"\n{x.YELLOW}>>{x.GREEN} {user['name']}{c.END}, {x.VIOLETBG}{c.WHITE}{decoded.n70}{c.END}")
        sleep(0.2)
        clear()

    def foo(force=False):
        if True or force:
            pass

#==================================================================#

def back(num = -1):
    WN = windowHistory[num]
    func = f"{WN}Menu()"
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
    global window
    global windowHistory

    window = string
    if window == windowHistory[-1]:
        return
    windowHistory.append(string)
    
#==================================================================#

def choiceCheck(thing:str):
    """Makes changes to the input to execute commands or place the placeholders."""


    # Placeholders:
    if "{" in thing and "}" in thing:
        if placeholders['nl'] in thing:
            thing = thing.replace(placeholders['nl'], f"\n{x.YELLOW}>>{x.VIOLET}=============================={x.YELLOW}<<{c.END}\n{x.VIOLET}>>{x.GRAY} ")
        if placeholders['br'] in thing:
            thing = thing.replace(placeholders['br'], "\n" + output.notify(f"", Print = False) + x.GRAY)
            
        if placeholders['name'] in thing:
            thing = thing.replace(placeholders['name'], str(user['name']))
        if placeholders['age'] in thing:
            thing = thing.replace(placeholders['age'], str(user['age']))
            
        if placeholders['prefix'] in thing:
            thing = thing.replace(placeholders['prefix'], str(settings['prefix']))
            
        if placeholders['lastTTTWinner'] in thing:
            thing = thing.replace(placeholders['lastTTTWinner'], str(apps['ttt']['last-winner']) + x.GRAY) 
        if placeholders['xWins'] in thing:
            thing = thing.replace(placeholders['xWins'], str(apps['ttt']['x-wins']) + x.GRAY)
        if placeholders['oWins'] in thing:
            thing = thing.replace(placeholders['oWins'], str(apps['ttt']['o-wins']) + x.GRAY)
        if placeholders['tttTies'] in thing:
            thing = thing.replace(placeholders['tttTies'], str(apps['ttt']['ties']) + x.GRAY)
        if placeholders['lastTTTBoard'] in thing:
            thing = thing.replace(placeholders['lastTTTBoard'], f"\n{ttt.displayBoard(apps['ttt']['last-board'], True, left=f'{x.VIOLET}>>{c.END} ')}{x.VIOLET}>>{x.GRAY} ")
        
        if placeholders['p1Last'] in thing:
            thing = thing.replace(placeholders['p1Last'], str(apps['rps']['p1']['last-choice']) + x.GRAY)
        if placeholders['p2Last'] in thing:
            thing = thing.replace(placeholders['p2Last'], str(apps['rps']['p2']['last-choice']) + x.GRAY)
        if placeholders['cpuLast'] in thing:
            thing = thing.replace(placeholders['cpuLast'], str(apps['rps']['cpu']['last-choice']) + x.GRAY)
        if placeholders['p1Wins'] in thing:
            thing = thing.replace(placeholders['p1Wins'], str(apps['rps']['p1']['wins']) + x.GRAY)
        if placeholders['p2Wins'] in thing:
            thing = thing.replace(placeholders['p2Wins'], str(apps['rps']['p2']['wins']) + x.GRAY)
        if placeholders['cpuWins'] in thing:
            thing = thing.replace(placeholders['cpuWins'], str(apps['rps']['cpu']['wins']) + x.GRAY)
        if placeholders['rpsTies'] in thing:
            thing = thing.replace(placeholders['rpsTies'], str(apps['rps']['ties']) + x.GRAY)
        if placeholders['lastRPSWinner'] in thing:
            thing = thing.replace(placeholders['lastRPSWinner'], str(apps['rps']['last-winner']) + x.GRAY)

        if placeholders['heads'] in thing:
            thing = thing.replace(placeholders['heads'], str(apps['rnd']['heads']) + x.GRAY)
        if placeholders['tails'] in thing:
            thing = thing.replace(placeholders['tails'], str(apps['rnd']['tails']) + x.GRAY)
        if placeholders['flips'] in thing:
            thing = thing.replace(placeholders['flips'], str(apps['rnd']['flips']) + x.GRAY)
        if placeholders['rndTies'] in thing:
            thing = thing.replace(placeholders['rndTies'], str(apps['rnd']['ties']) + x.GRAY)
        if placeholders['lastHeads'] in thing:
            thing = thing.replace(placeholders['lastHeads'], str(apps['rnd']['last-heads']) + x.GRAY)
        if placeholders['lastTails'] in thing:
            thing = thing.replace(placeholders['lastTails'], str(apps['rnd']['last-tails']) + x.GRAY)
        if placeholders['lastFlips'] in thing:
            thing = thing.replace(placeholders['lastFlips'], str(apps['rnd']['last-flips']) + x.GRAY)
        if placeholders['lastRNDWinner'] in thing:
            thing = thing.replace(placeholders['lastRNDWinner'], str(apps['rnd']['last-winner']) + x.GRAY)
            
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
        thing = thing.replace("SPAIME", f"{x.YELLOW}[{x.VIOLET}SPAIME{x.YELLOW}]" + x.GRAY)
    if "SPAIME-2" in thing:
        thing = thing.replace("SPAIME-2", f"{x.YELLOW}[{x.VIOLET}SPAIME{x.YELLOW}]²" + x.GRAY)
    if "Shrek" in thing:
        thing = thing.replace("Shrek", x.GREEN + "Shrek" + x.GRAY)

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
                    print(f"\n{x.ORANGE}>>>{x.VIOLET} Hey boss! What do you wish to do?{c.END}")
                    dev = input(f"\n{x.ORANGE}1 >{x.LETTUCE} ")
                    print(c.END)

                    try:
                        print(eval(dev))
                        print("")
                    except NameError:
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
                    print(f"\n{x.ORANGE}>>>{x.VIOLET} Hey boss! What do you wish to do?{c.END}")
                    dev = input(f"\n{x.ORANGE}2 >{x.LETTUCE} ")
                    print(c.END)

                    try:
                        print(exec(dev))
                        print("")
                    except NameError:
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
    bricks = "{}"

    print()
    if user['name'] in ('', None):
        output.stamp(f"Hey there! Whatcha wanna do?!")
    else:
        output.stamp(f"Hey there, {x.GREEN}{user['name']}{x.VIOLET}! Whatcha wanna do?!")
    output.note(1, settings['prefix'])
    print()
    
    output.option(1, f"{x.GRAY}[{x.LETTUCE}↑↓{x.GRAY}] Repeat")
    output.option(2, f"{x.GRAY}[{x.LETTUCE}π*{x.GRAY}] Math & Logic")
    output.option(3, f"{x.GRAY}[{x.LETTUCE}☘{x.YELLOW}%{x.GRAY}] Randomeur")
    output.option(4, f"{x.GRAY}[{x.LETTUCE}$${x.GRAY}] RockPaperScissors")
    output.option(5, f"{x.GRAY}[{ttt.s.x}{ttt.s.o}{x.GRAY}] TicTacToe")
    output.option(6, f"{x.GRAY}[{msp.flagS}{msp.bombS}{x.GRAY}] Minesweeper")
    output.option(7, f"{x.GRAY}[{x.YELLOW}{bricks}{x.GRAY}] Options")
    output.option(8, f"{x.GRAY}[{x.VIOLET}>>{x.GRAY}] Credits")
    output.option(9, f"{x.GRAY}[{x.RED}x{x.GREEN}✓{x.GRAY}] Refresh")
    output.option(0, f"{x.GRAY}[{x.RED}xx{x.GRAY}] Exit")
    
    choice = intake.prompt()
    choice = choiceCheck(choice)

    # El Menus
    if choice == "1":
        clear()
        repeatMenu()
    if choice == "2":
        clear()
        mathMenu()
    if choice == "3":
        clear()
        rndMenu()
    if choice == "4":
        clear()
        rpsMenu()
    if choice == "5":
        clear()
        tttMenu()
    if choice == "6":
        clear()
        mspMenu()
    if choice == "7":
        clear()
        optionsMenu()
    if choice == "8":
        clear()
        infoF()
    if choice == "9":
        clear()
        refreshF()
    if choice == "0":
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
        print(f" {x.YELLOW}-{c.END} " + f"Total {rnd.headsStyle}{c.END}: {x.GRAY}{apps['rnd']['heads']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"Total {rnd.tailsStyle}{c.END}: {x.GRAY}{apps['rnd']['tails']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"Total {rnd.flipsStyle}{c.END}: {x.GRAY}{apps['rnd']['flips']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"Total {rnd.tieStyle}{x.RED}s{c.END}:  {x.GRAY}{apps['rnd']['ties']}{c.END}")
        print(f"")
        print(f" {x.YELLOW}-{c.END} " + f"Last {rnd.headsStyle}{c.END}:  {x.GRAY}{apps['rnd']['last-heads']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"Last {rnd.tailsStyle}{c.END}:  {x.GRAY}{apps['rnd']['last-tails']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"Last {rnd.flipsStyle}{c.END}:  {x.GRAY}{apps['rnd']['last-flips']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"Last Winner{c.END}: {x.GRAY}{apps['rnd']['last-winner']}{c.END}")
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
        
        wins = [
            apps['rps']['cpu']['wins'], apps['rps']['p1']['wins'], apps['rps']['p2']['wins']
        ]
        name = [   
            rps.cpu['name'], rps.p1['name'], rps.p2['name']
        ]
        
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
        print(f" {x.YELLOW}-{c.END} " + f"{rps.p1['name']} Wins        : {x.GRAY}{apps['rps']['p1']['wins']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"{rps.p1['name']} Last Choice : {x.GRAY}{apps['rps']['p1']['last-choice']}{c.END}")
        print()
        print(f" {x.YELLOW}-{c.END} " + f"{rps.p2['name']} Wins        : {x.GRAY}{apps['rps']['p2']['wins']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"{rps.p2['name']} Last Choice : {x.GRAY}{apps['rps']['p2']['last-choice']}{c.END}")
        print()
        print(f" {x.YELLOW}-{c.END} " + f"{rps.cpu['name']} Wins        : {x.GRAY}{apps['rps']['cpu']['wins']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"{rps.cpu['name']} Last Choice : {x.GRAY}{apps['rps']['cpu']['last-choice']}{c.END}")
        print()
        print(f" {x.YELLOW}-{c.END} " + f"Ties : {x.GRAY}{apps['rps']['ties']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"Best : {x.GRAY}{whosBest()}{c.END}")
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
        output.option(2, "Difficulty: " + x.LETTUCE + apps['ttt']['diff'])
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
            output.stamp(f"What do you want the difficulty to be? {x.LETTUCE}(H,M,E)")
            output.note(1, settings['prefix'])
            output.note(f"Current is {x.LETTUCE}{apps['ttt']['diff']}{c.END}")
            print()
            allowed = "HME"
            choice = intake.prompt()
            choice = choiceCheck(choice)
            if goThro(choice.upper(), allowed) and len(choice) == 1:
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
        output.stamp(f"TicTacToe Statistics:\n{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"X Wins     : {x.GRAY}{apps['ttt']['x-wins']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"O Wins     : {x.GRAY}{apps['ttt']['o-wins']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"Ties       : {x.GRAY}{apps['ttt']['ties']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"Last Winner: {x.GRAY}{apps['ttt']['last-winner']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"Last Board :-\n")
        print(ttt.displayBoard(apps['ttt']['last-board'], True, left=f' {x.YELLOW}-{c.END} '))
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
            if winner == ttt.s.n:
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
        output.option(1, "Map Size: " + x.LETTUCE + str(apps['msp']['dim']) + c.END)
        output.option(2, "Bomb Count: " + x.LETTUCE + str(apps['msp']['bombC']) + c.END)
        output.option(0, "Back")
        
        choice = intake.prompt()
        choice = choiceCheck(choice)
        
        if choice == "1":
            clear()
            print()
            output.stamp("What do you want the map size to be?")
            output.note(1, settings['prefix'])
            output.note(f"Map size ranges from {x.YELLOW}1:99{c.END}")
            output.note(f"I don't recommend anything above 25 for your machine's health, also I do not recommend anything above 10 for the looks of it.")
            output.note(f"Current is {x.LETTUCE}{apps['msp']['dim']}{c.END}")
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
            output.note(f"Bombs count ranges from {x.YELLOW}1:{apps['msp']['dim']**2}{x.END}")
            output.note(f"Current is {x.LETTUCE}{apps['msp']['bombC']}{c.END}")
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
        back(-2)

    def statsMenu():
        print()
        output.stamp(f"Minesweeper Statistics:\n")
        print(f" {x.YELLOW}-{c.END} " + f"Total Wins :     {x.GRAY}{apps['msp']['wins']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"Total Loses:     {x.GRAY}{apps['msp']['defeats']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"Total Dug Spots: {x.GRAY}{apps['msp']['spots-dug']}{c.END}")
        print(f" {x.YELLOW}-{c.END} " + f"Last Map:-")
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
        back()
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
    output.option(1, f"Name: {x.GREEN}{user['name'] if user['name'] != '' else 'N/A'}")
    output.option(2, f"Gender: {x.GREEN}{user['sex'] if user['sex'] != None else 'N/A'}")
    output.option(3, f"Age: {x.GREEN}{user['age']}")
    output.option(4, f"Prefix: {x.GREEN}{settings['prefix']}")
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
        output.note(f"Current is {x.GREEN}{user['name'] if user['name'] != '' else 'N/A'}")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        nameChange(choice)

        back()

    elif choice == "3" or choice.casefold() == "age":

        clear()
        print()
        output.stamp(f"How old are you?")
        output.note(1, settings['prefix'])
        output.note(f"Current is {x.GREEN}{user['age']}")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        ageChange(choice)

        back()
    elif choice == "2" or choice.casefold() == "gender":

        clear()
        print()
        output.stamp(f"Cation, Anion or Zwitterion? {x.LETTUCE}(M,F,N)")
        output.note(1, settings['prefix'])
        output.note(f"Current is {x.GREEN}{user['sex'] if user['sex'] != None else 'N/A'}")
        
        choice = intake.prompt()
        choice = choiceCheck(choice)

        sexChange(choice)

        back()
    elif choice == "4" or choice.casefold() == "prefix":

        clear()
        print()
        output.stamp(f"Set prefix to what?")
        output.note(1, settings['prefix'])
        output.note(f"Current is {x.GREEN}{settings['prefix']}")
        
        choice = intake.prompt()
        choice = choiceCheck(choice)
        
        prefix_change(choice)

        back()
    elif choice == "8" or choice.casefold() == "reset stats":
        
        clear()
        output.notify(f"Continuing would mean you want to reset statistics to default.")
        if confirm(output.notify(f"Are you sure?", Print=False)):
            print()
            output.notify(f"Please type {x.GRAY}{c.ITALIC}\"{x.LETTUCE}{settings['prefix']}reset{x.GRAY}\"{c.END}{x.GRAY} to further confirm.")

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
            output.notify(f"Please type {x.GRAY}{c.ITALIC}\"{x.LETTUCE}{settings['prefix']}reset{x.GRAY}\"{c.END}{x.GRAY} to further confirm.")

            choice = intake.prompt()
            choice = choiceCheck(choice)

            if choice == f"{settings['prefix']}reset":
                resetYAML()
                resetPICKLE()
                clear()
                output.success(f"All done, good as new. {c.END}")
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
    print(f" {x.YELLOW}-{c.END} {settings['prefix']}" + f"help [┬]   : {x.GRAY}Shows this menu.{c.END}")
    print(                                          f"          ├math: {x.GRAY}Shows help about Math & Logic.{c.END}")
    print(                                          f"          ├rnd : {x.GRAY}Shows help about Randomeur.{c.END}")
    print(                                          f"          ├rps : {x.GRAY}Shows help about RockPaperScissors.{c.END}")
    print(                                          f"          ├ttt : {x.GRAY}Shows help about TicTacToe.{c.END}")
    print(                                          f"          └msp : {x.GRAY}Shows help about Minesweeper.{c.END}")
    print(f" {x.YELLOW}-{c.END} {settings['prefix']}" + f"back:        {x.GRAY}Returns you a page back.{c.END}")
    print(f" {x.YELLOW}-{c.END} {settings['prefix']}" + f"home:        {x.GRAY}Returns you to home page.{c.END}")
    print(f" {x.YELLOW}-{c.END} {settings['prefix']}" + f"refr:        {x.GRAY}Refreshes current page.{c.END}")
    print(f" {x.YELLOW}-{c.END} {settings['prefix']}" + f"exit:        {x.GRAY}To safely exit the app.{c.END}")
    print(f" {x.YELLOW}-{c.END} {settings['prefix']}" + f"dev1:        {x.GRAY}Enters eval() mode. {x.RED}{c.DIM}(dev-only){c.END}")
    print(f" {x.YELLOW}-{c.END} {settings['prefix']}" + f"dev2:        {x.GRAY}Enters exec() mode. {x.RED}{c.DIM}(dev-only){c.END}")
    print("\n")
    output.stamp(f"Placeholders:")
    # The available placeholders.
               # The syntax ones.
    print(f" {x.YELLOW}-{c.END}" + " {nl}: " + f"           {x.GRAY}Makes a lovely line separator, not useful.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {br}: " + f"           {x.GRAY}Makes a new line, useful in repeat, I guess.{c.END}")
    print(f"") # The user & settings ones.
    print(f" {x.YELLOW}-{c.END}" + " {name}: " + f"         {x.GRAY}Returns your name.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {age}: " + f"          {x.GRAY}Returns your age.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {prefix}: " + f"       {x.GRAY}Returns set prefix{c.END}")
    print(f"") # The math & physics ones.
    print(f" {x.YELLOW}-{c.END}" + " {e}: " + f"            {x.GRAY}Returns Euler's number's value.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {g}: " + f"            {x.GRAY}Returns gravitational acceleration constant's value.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {pi}: " + f"           {x.GRAY}Returns pi's value.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {tau}: " + f"          {x.GRAY}Returns tau's value.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {phi}: " + f"          {x.GRAY}Returns the golden ratio's value.{c.END}")
    print(f"") # The Randomeur ones.
    print(f" {x.YELLOW}-{c.END}" + " {heads}: " + f"        {x.GRAY}Returns the total amount of {rnd.headsStyle}{x.GRAY}.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {tails}: " + f"        {x.GRAY}Returns the total amount of {rnd.tailsStyle}{x.GRAY}.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {rndTies}: " + f"      {x.GRAY}Returns the total amount of RND {rnd.tieStyle}{x.RED}s{x.GRAY}.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {flips}: " + f"        {x.GRAY}Returns the total amount of RND {rnd.flipsStyle}{x.GRAY}.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {lastHeads}: " + f"    {x.GRAY}Returns the last {rnd.headsStyle}{x.GRAY} count.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {lastTails}: " + f"    {x.GRAY}Returns the last {rnd.tailsStyle}{x.GRAY} count.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {lastFlips}: " + f"    {x.GRAY}Returns the last {rnd.flipsStyle}{x.GRAY} count.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {lastRNDWinner}: " + f"{x.GRAY}Returns the last RND winner.{c.END}")
    print(f"") # The RockPaperScissors ones.
    print(f" {x.YELLOW}-{c.END}" + " {p1Last}: " + f"       {x.GRAY}Returns {rps.p1['name']}{x.GRAY} last move.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {p2Last}: " + f"       {x.GRAY}Returns {rps.p2['name']}{x.GRAY} last move.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {cpuLast}: " + f"      {x.GRAY}Returns {rps.cpu['name']}{x.GRAY} last move.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {p1Wins}: " + f"       {x.GRAY}Returns how many times {rps.p1['name']}{x.GRAY} won.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {p2Wins}: " + f"       {x.GRAY}Returns how many times {rps.p2['name']}{x.GRAY} won.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {cpuWins}: " + f"      {x.GRAY}Returns how many times {rps.cpu['name']}{x.GRAY} won.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {rpsTies}: " + f"      {x.GRAY}Returns how many times RPS ties happened.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {lastRPSWinner}: " + f"{x.GRAY}Returns the last RPS winner.{c.END}")
    print(f"") # The TicTacToe ones.
    print(f" {x.YELLOW}-{c.END}" + " {lastTTTWinner}: " + f"{x.GRAY}Returns the last TTT winner.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {lastTTTBoard}: " + f" {x.GRAY}Returns the last TTT board.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {xWins}: " + f"        {x.GRAY}Returns how many times x won.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {oWins}: " + f"        {x.GRAY}Returns how many times o won.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {tttTies}: " + f"      {x.GRAY}Returns how many TTT ties happened.{c.END}")
    print(f"") # The Minesweeper ones.
    print(f" {x.YELLOW}-{c.END}" + " {mspWins}: " + f"      {x.GRAY}Returns how many times you won at MSP.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {mspDefeats}: " + f"   {x.GRAY}Returns how many times you lost at MSP.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {mspDug}: " + f"       {x.GRAY}Returns how many times you dug manually at MSP.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {mspBombs}: " + f"     {x.GRAY}Returns how many bombs are in MSP config.{c.END}")
    print(f" {x.YELLOW}-{c.END}" + " {mspSize}: " + f"      {x.GRAY}Returns how big the map is in MSP config.{c.END}")

    enterContinue()

#==================================================================#

def helpMathF():

    print()
    output.stamp("Math & Logic Help:")

    output.note(f"You can use basic math and logic gates.", sign="D")
    output.note(f'Allowed Input: "{x.LETTUCE}0123456789+-*×x/\\÷^.,()%=TF!&| {c.END}{x.GRAY}".', sign="D")
    output.note(f"T  {x.LETTUCE}->{x.GRAY} True", sign="D")
    output.note(f"F  {x.LETTUCE}->{x.GRAY} False", sign="D")
    output.note(f"!  {x.LETTUCE}->{x.GRAY} not", sign="D")
    output.note(f"&  {x.LETTUCE}->{x.GRAY} and", sign="D")
    output.note(f"|  {x.LETTUCE}->{x.GRAY} or", sign="D")
    output.note(f"== {x.LETTUCE}->{x.GRAY} equal-to", sign="D")
    output.note(f"!= {x.LETTUCE}->{x.GRAY} not-equal-to", sign="D")

    enterContinue()

#==================================================================#

def helpRNDF():

    print()
    output.stamp("Randomeur Help:")

    print()
    output.notify("Flipeur:")

    output.note(f"Flip a coin for [{x.LETTUCE}x-amount{x.GRAY}] of times.", sign="D")
    output.note(f"[{x.LETTUCE}x-amount{x.GRAY}] must be between {x.LETTUCE}1:10000.", sign="D")
    output.note(f"That is so you don't smell a grilled CPU core.", sign="D")
    output.note(f"Check on the statistics to see some cool figures.", sign="D")

    enterContinue()

#==================================================================#

def helpRPSF():
    print()
    output.stamp("RockPaperScissors Help:")
    output.note(f"There're two main modes:", sign="D")
    output.note(f"You choose rock, paper or scissors and the CPU randomizes a choice.", sign=f"{x.YELLOW}Solo:")
    output.note(f"You choose rock, paper or scissors and call a friend to choose too.", sign=f"{x.YELLOW}Duo :")
    output.note(f"Check on the statistics to see some cool figures.", sign="D")

    enterContinue()

#==================================================================#

def helpTTTF():
    print()
    output.stamp("TicTacToe Help:")
    output.note(f"First, choose whether to start with {ttt.s.x}{x.GRAY} or {ttt.s.o}{x.GRAY}.", sign="D")
    output.note(f"Next, just type the position number you want to play at.", sign="D")
    output.note(f"Check on the statistics to see some cool figures.", sign="D")

    enterContinue()

#==================================================================#

def helpMSPF():
    print()
    output.stamp("Minesweeper Help:")
    output.note(f"Boom!! {msp.bombS}", sign="D")
    output.note(f"Let's start by talking about the Config page.", sign="D")
    output.note(f"There you can choose the map size and the amount of bombs.", sign="D")
    output.note(f"To dig a spot just type {c.ITALIC}'[{x.LETTUCE}x,y{x.GRAY}]'{c.END}{x.GRAY} of that spot.", sign="D")
    output.note(f"To flag a spot just type {c.ITALIC}'[{x.LETTUCE}x,y{x.GRAY}]{msp.flagS}'{c.END}{x.GRAY} of that spot.", sign="D")
    output.note("Any brackets like (), [] or {}, and spaces are ignored.", sign="D")
    output.note(f"{msp.emptyS} {x.LETTUCE}->{x.GRAY} Not Dug", sign="D")
    output.note(f"{msp.nS[ random.randint(0,len(msp.nS)) -1 ]} {x.LETTUCE}->{x.GRAY} Dug", sign="D")
    output.note(f"{msp.flagS} {x.LETTUCE}->{x.GRAY} Flagged", sign="D")
    output.note(f"{msp.bombS} {x.LETTUCE}->{x.GRAY} Bomb", sign="D")
    output.note(f"Check on the statistics to see some cool figures.", sign="D")

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
        + x.LETTUCE + logo_art + c.END
        + x.VIOLET + logo_text + c.END
        + c.DIM
        + x.GRAY + logo_motto + c.END
        )

    # Your usual yadda yadda.
    print()
    output.stamp(f"SPAIME²")
    output.option(f"Version", f"x.x.x{c.END}")
    output.option(f"Author", f" Fastre{c.END}")
    output.option(f"Github", f" {c.URL}{c.ITALIC}https://github.com/IamFastre{c.END}")
    output.option(f"Discord", f"{c.URL}{c.ITALIC}https://discord.gg/kkzmxkG{c.END}")
    output.option(f"Note", f"   There was never a SPAIME¹{c.END}")
    choice = enterContinue()

    # An easter egg!
    if choice.casefold() in admins:
        output.success(f"Yes, {x.RED}♥{x.GRAY}.{c.END}")
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

    print(f"{x.YELLOW}>>{x.GRAY} Okie!{c.END}")
    sleep(0.5)
    clear()

    # Telling you sweet goodbyes.
    if user['name'] == '':
        output.notify(f"Bye-bye{x.VIOLET}!")
    else:
        output.notify(f"Bye-bye, {x.GREEN}{user['name']}{x.VIOLET}!")

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
    print(x.END)

#==================================================================#