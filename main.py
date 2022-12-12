# Importing the other py files.
from scripts.libs import *

#==================================================================#

# Importing the applets
import scripts.content.TicTacToe            as ttt
import scripts.content.RockPaperScissors    as rps
import scripts.content.Randomeur            as rnd
import scripts.content.Minesweeper          as msp
import scripts.content.Blackjack            as bjk
import scripts.content.Sudoku               as sdk
import scripts.content.BrainfuckInterpreter as bfi

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


DATA_DIR   = "./data/"
DEFAULTS   = "./data/.default/"

DATA_LIST     = os.listdir(DATA_DIR)
DEFAULT_LIST  = os.listdir(DEFAULTS)

YAML_REGEX = r'(?i).*?\.y(a?)ml(?!.)'
BIN_REGEX  = r'(?i).*?\.bin(?!.)'


def Update():
    global DATA_LIST

    DATA_LIST  = os.listdir(DATA_DIR)
    try:
        readYAML()
        readBINARY()
    except Exception as error:
        errorSTR = re.sub(r"\[Errno\W\d+\]\W", '', str(error))
        output.error("I think an error have occurred...")
        output.error(errorSTR)
        if confirm(output.error(f"Wanna continue? (I don't recommend)", 0)):
            clear()
            output.error("Ok whatever...")
            sleep(2)
        else:
            try:
                exitF()
            except NameError:
                clear()
                output.notify("Welp, bye!")
                sys.exit(0)
    
    return True
    

####################################################################
##                                                                ##
## Loading the YAML & Pickle files and defining their functions.  ##
##                                                                ##
####################################################################

YAML:dict = {}
BIN :dict = {}
FILES:list = [YAML, BIN]

def dataFileDub(file):
    output.error(f"There might be a data file name duplicate: {file}.")
    output.error(f"I recommend you consider renaming.")
    output.note( f"The latter will overwrite the former.")

    enterContinue()


def readYAML():
    """I hate this function so much."""

    YAML_FILES = list(
        filter(
            re.compile(YAML_REGEX).match,
            DATA_LIST
            )
        )

    # That's very human-readable:
    FILE_COUNT:list = []
    for file in YAML_FILES:
        index = re.sub(YAML_REGEX.replace('.*?', ''),'', file)

        if index not in FILE_COUNT: FILE_COUNT.append(index)
        else: dataFileDub(file)

        with open(DATA_DIR + file, 'r') as yamlFile:
            YAML[index]  = yaml.safe_load(yamlFile)

#==================================================================#

def writeYAML():
    """I hate this function so much."""

    YAML_FILES = list(
        filter(
            re.compile(YAML_REGEX).match,
            DATA_LIST
            )
        )

    # That's very human-readable:
    for file in YAML_FILES:
        with open(DATA_DIR + file, 'w') as yamlFile:
            index = re.sub(YAML_REGEX.replace('.*?', ''),'', file)
            yaml.safe_dump(YAML[index], yamlFile)

#==================================================================#

def readBINARY():
    """I do too hate this function."""

    BIN_FILES = list(
        filter(
            re.compile(BIN_REGEX).match,
            DATA_LIST
            )
        )

    # That's very human-readable:
    FILE_COUNT:list = []
    for file in BIN_FILES:
        index = re.sub(BIN_REGEX.replace('.*?', ''),'', file)

        if index not in FILE_COUNT: FILE_COUNT.append(index)
        else: dataFileDub(file)

        with open(DATA_DIR + file, 'rb') as binFile:
            BIN[index]  = pickle.load(binFile)

#==================================================================#

def writeBINARY():
    """I do too hate this function."""

    BIN_FILES = list(*[BIN] if len(BIN) > 1 else [BIN])
    # That's very human-readable:
    for file in BIN_FILES:
        with open(DATA_DIR + file + '.bin', 'wb') as binFile:
            pickle.dump(BIN[file], binFile)

#==================================================================#

def resetDATA(_dict:dict = None, _key:str = r'.*?'):
    if _dict == YAML: _regex = r'\.y(a?)ml(?!.)'
    if _dict == BIN : _regex = r'\.bin(?!.)'

    if _dict == None:
        for file in DEFAULT_LIST:
            shutil.copy(DEFAULTS + file, DATA_DIR + file)
        return

    _files = list(
        filter(
            re.compile(r'(?i)'+_key+_regex).match,
            DEFAULT_LIST
            )
        )


    for file in _files:
        shutil.copy(DEFAULTS + file, DATA_DIR + file)

#==================================================================#

def writeDATA(_name:str, _data:dict):
    if _data not in FILES: raise TypeError("Unsupported DATA file type.")
    if _data == YAML: _extension = 'yaml'; _mode = 'w'
    if _data == BIN : _extension = 'bin'; _mode = 'wb'

    _extension = '.' + _extension
    with open(DATA_DIR + _name + _extension, _mode) as _file:
        if _mode == 'w':  yaml.safe_dump(_data[_name], _file)
        if _mode == 'wb': pickle.dump(_data[_name], _file)

#==================================================================#

if __name__ == '__main__': Update()
BIN['Sudoku'] = sdk.Sudoku(0)
BIN["Sudoku"].playable = 0
BIN["Sudoku"].default  = 1
writeDATA('Sudoku', BIN)

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
YAML['Settings']['LastDate'] = today

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
    return (YAML['Settings']['Name'].casefold() in admins and YAML['Settings']['Age'] in passes and YAML['Settings']['Sex'] == "Male")

#==================================================================#

def isCommand(thing):
    global commands

    commands = [
        YAML['Settings']['Prefix'] + "help",
        YAML['Settings']['Prefix'] + "help math",
        YAML['Settings']['Prefix'] + "help rnd",
        YAML['Settings']['Prefix'] + "help rps",
        YAML['Settings']['Prefix'] + "help ttt",
        YAML['Settings']['Prefix'] + "help msp",
        YAML['Settings']['Prefix'] + "help bjk",
        YAML['Settings']['Prefix'] + "help sdk",

        YAML['Settings']['Prefix'] + "back",
        YAML['Settings']['Prefix'] + "home",
        YAML['Settings']['Prefix'] + "exit",
        YAML['Settings']['Prefix'] + "refr",

        YAML['Settings']['Prefix'] + "dev1",
        YAML['Settings']['Prefix'] + "dev2",

        YAML['Settings']['Prefix'] + "reset",
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
            if YAML['Settings']['Name'] == '':
                print(f"\n{X0.YELLOW}>> {X0.VIOLETBG}{C0.WHITE}{decoded.n69}{C0.END}")
            else:
                print(f"\n{X0.YELLOW}>>{X0.GREEN} {YAML['Settings']['Name']}{C0.END}, {X0.VIOLETBG}{C0.WHITE}{decoded.n69}{C0.END}")
        else:
            if YAML['Settings']['Name'] == '':
                print(f"\n{X0.YELLOW}>> {X0.VIOLETBG}{C0.WHITE}{decoded.n70}{C0.END}")
            else:
                print(f"\n{X0.YELLOW}>>{X0.GREEN} {YAML['Settings']['Name']}{C0.END}, {X0.VIOLETBG}{C0.WHITE}{decoded.n70}{C0.END}")
        sleep(0.2)
        clear()

    def foo(force=False):
        if True or force:
            pass


#==================================================================#

def back(num = -1):
    WN = windowHistory[num]
    func = f"{WN}Menu()"

    Update()

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
    
    Update()

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
            thing = thing.replace(placeholders['name'], str(YAML['Settings']['Name']))
        if placeholders['age'] in thing:
            thing = thing.replace(placeholders['age'], str(YAML['Settings']['Age']))

        if placeholders['prefix'] in thing:
            thing = thing.replace(placeholders['prefix'], str(YAML['Settings']['Prefix']))

        if placeholders['lastTTTWinner'] in thing:
            thing = thing.replace(placeholders['lastTTTWinner'], str(YAML['TicTacToe']['LastWinner']) + X0.GRAY) 
        if placeholders['xWins'] in thing:
            thing = thing.replace(placeholders['xWins'], str(YAML['TicTacToe']['xWins']) + X0.GRAY)
        if placeholders['oWins'] in thing:
            thing = thing.replace(placeholders['oWins'], str(YAML['TicTacToe']['oWins']) + X0.GRAY)
        if placeholders['tttTies'] in thing:
            thing = thing.replace(placeholders['tttTies'], str(YAML['TicTacToe']['Ties']) + X0.GRAY)
        if placeholders['lastTTTBoard'] in thing:
            thing = thing.replace(placeholders['lastTTTBoard'], f"\n{ttt.displayBoard(YAML['TicTacToe']['LastBoard'], True, left=f'{X0.VIOLET}>>{C0.END} ')}{X0.VIOLET}>>{X0.GRAY} ")

        if placeholders['p1Last'] in thing:
            thing = thing.replace(placeholders['p1Last'], str(YAML['RockPaperScissors']['P1']['LastChoice']) + X0.GRAY)
        if placeholders['p2Last'] in thing:
            thing = thing.replace(placeholders['p2Last'], str(YAML['RockPaperScissors']['P2']['LastChoice']) + X0.GRAY)
        if placeholders['cpuLast'] in thing:
            thing = thing.replace(placeholders['cpuLast'], str(YAML['RockPaperScissors']['CPU']['LastChoice']) + X0.GRAY)
        if placeholders['p1Wins'] in thing:
            thing = thing.replace(placeholders['p1Wins'], str(YAML['RockPaperScissors']['P1']['Wins']) + X0.GRAY)
        if placeholders['p2Wins'] in thing:
            thing = thing.replace(placeholders['p2Wins'], str(YAML['RockPaperScissors']['P2']['Wins']) + X0.GRAY)
        if placeholders['cpuWins'] in thing:
            thing = thing.replace(placeholders['cpuWins'], str(YAML['RockPaperScissors']['CPU']['Wins']) + X0.GRAY)
        if placeholders['rpsTies'] in thing:
            thing = thing.replace(placeholders['rpsTies'], str(YAML['RockPaperScissors']['Ties']) + X0.GRAY)
        if placeholders['lastRPSWinner'] in thing:
            thing = thing.replace(placeholders['lastRPSWinner'], str(YAML['RockPaperScissors']['LastWinner']) + X0.GRAY)

        if placeholders['heads'] in thing:
            thing = thing.replace(placeholders['heads'], str(YAML['Randomeur']['Heads']) + X0.GRAY)
        if placeholders['tails'] in thing:
            thing = thing.replace(placeholders['tails'], str(YAML['Randomeur']['Tails']) + X0.GRAY)
        if placeholders['flips'] in thing:
            thing = thing.replace(placeholders['flips'], str(YAML['Randomeur']['Flips']) + X0.GRAY)
        if placeholders['rndTies'] in thing:
            thing = thing.replace(placeholders['rndTies'], str(YAML['Randomeur']['Ties']) + X0.GRAY)
        if placeholders['lastHeads'] in thing:
            thing = thing.replace(placeholders['lastHeads'], str(YAML['Randomeur']['LastHeads']) + X0.GRAY)
        if placeholders['lastTails'] in thing:
            thing = thing.replace(placeholders['lastTails'], str(YAML['Randomeur']['LastTails']) + X0.GRAY)
        if placeholders['lastFlips'] in thing:
            thing = thing.replace(placeholders['lastFlips'], str(YAML['Randomeur']['LastFlips']) + X0.GRAY)
        if placeholders['lastRNDWinner'] in thing:
            thing = thing.replace(placeholders['lastRNDWinner'], str(YAML['Randomeur']['LastWinner']) + X0.GRAY)

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
            thing = thing.replace(placeholders['mspWins'], str(YAML['Minesweeper']['Wins']))
        if placeholders['mspDefeats'] in thing:
            thing = thing.replace(placeholders['mspDefeats'], str(YAML['Minesweeper']['Defeats']))
        if placeholders['mspDug'] in thing:
            thing = thing.replace(placeholders['mspDug'], str(YAML['Minesweeper']['SpotsDug']))
        if placeholders['mspBombs'] in thing:
            thing = thing.replace(placeholders['mspBombs'], str(YAML['Minesweeper']['BombCount']))
        if placeholders['mspSize'] in thing:
            thing = thing.replace(placeholders['mspSize'], str(YAML['Minesweeper']['Dimension']))

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
    if thing.startswith(YAML['Settings']['Prefix']):
        cmd = thing.replace(YAML['Settings']['Prefix'], "")

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
            clear()
            output.error(f"Please do {YAML['Settings']['Prefix']}dev2 instead.")
            back()

        if cmd == "dev2":

            if isAdmin():
                clear()
                print(f"\n{X0.ORANGE}>>>{X0.VIOLET} Hey boss! What do you wish to do?{C0.END}")

                def debug1():
                    dev = input(
                        output.arrow("", X0.ORANGE + '1>', 1, Print=0)
                    )

                    try:
                        exec(dev)
                        output.notify(eval(dev))
                    except BaseException as Error:
                        print(Error)
                        debug1()
                        back()
                    else:
                        debug1()

                debug1()

            else:
                clear()
                output.error("It's a dev-only commands, buddy.")
                back()

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
    if YAML['Settings']['Name'] in ('', None):
        output.stamp(f"Hey there! Whatcha wanna do?!")
    else:
        output.stamp(f"Hey there, {X0.GREEN}{YAML['Settings']['Name']}{X0.VIOLET}! Whatcha wanna do?!")
    output.note(1, YAML['Settings']['Prefix'])
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
    output.note(1, YAML['Settings']['Prefix'])

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
    output.note(1, YAML['Settings']['Prefix'])

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
        print(f" {X0.YELLOW}-{C0.END} " + f"Total {rnd.headsStyle}{C0.END}: {X0.GRAY}{YAML['Randomeur']['Heads']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total {rnd.tailsStyle}{C0.END}: {X0.GRAY}{YAML['Randomeur']['Tails']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total {rnd.flipsStyle}{C0.END}: {X0.GRAY}{YAML['Randomeur']['Flips']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total {rnd.tieStyle}{X0.RED}s{C0.END}:  {X0.GRAY}{YAML['Randomeur']['Ties']}{C0.END}")
        print(f"")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last {rnd.headsStyle}{C0.END}:  {X0.GRAY}{YAML['Randomeur']['LastHeads']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last {rnd.tailsStyle}{C0.END}:  {X0.GRAY}{YAML['Randomeur']['LastTails']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last {rnd.flipsStyle}{C0.END}:  {X0.GRAY}{YAML['Randomeur']['LastFlips']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last Winner{C0.END}: {X0.GRAY}{YAML['Randomeur']['LastWinner']}{C0.END}")
        enterContinue()

    def statsReset():
        if confirm(output.notify(f"Are you sure?", Print= False)):
            resetDATA(YAML, 'Randomeur')
            clear()
            output.success(f"All done, good as new.")
            back()
        else:
            clear()
            output.error(f"Okay then.")
            back()

    print()
    output.stamp(f"Welcome to Randomeur!")
    output.note(1, YAML['Settings']['Prefix'])
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

        YAML['Randomeur']['Heads']    += rnd.heads
        YAML['Randomeur']['Tails']    += rnd.tails
        YAML['Randomeur']['Flips']    += rnd.flips
        if rnd.heads == rnd.tails:
            YAML['Randomeur']['Ties'] += 1
        writeYAML()

        YAML['Randomeur']['LastHeads']       = rnd.heads
        YAML['Randomeur']['LastTails']       = rnd.tails
        YAML['Randomeur']['LastFlips']       = rnd.flips
        writeYAML()

        YAML['Randomeur']['LastWinner']      = rnd.winner
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

        wins = [YAML['RockPaperScissors']['CPU']['Wins'], YAML['RockPaperScissors']['P1']['Wins'], YAML['RockPaperScissors']['P2']['Wins']]
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
        print(f" {X0.YELLOW}-{C0.END} " + f"{rps.p1['name']} Wins        : {X0.GRAY}{YAML['RockPaperScissors']['P1']['Wins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"{rps.p1['name']} Last Choice : {X0.GRAY}{YAML['RockPaperScissors']['P1']['LastChoice']}{C0.END}")
        print()
        print(f" {X0.YELLOW}-{C0.END} " + f"{rps.p2['name']} Wins        : {X0.GRAY}{YAML['RockPaperScissors']['P2']['Wins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"{rps.p2['name']} Last Choice : {X0.GRAY}{YAML['RockPaperScissors']['P2']['LastChoice']}{C0.END}")
        print()
        print(f" {X0.YELLOW}-{C0.END} " + f"{rps.cpu['name']} Wins        : {X0.GRAY}{YAML['RockPaperScissors']['CPU']['Wins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"{rps.cpu['name']} Last Choice : {X0.GRAY}{YAML['RockPaperScissors']['CPU']['LastChoice']}{C0.END}")
        print()
        print(f" {X0.YELLOW}-{C0.END} " + f"Ties : {X0.GRAY}{YAML['RockPaperScissors']['Ties']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Best : {X0.GRAY}{whosBest()}{C0.END}")
        enterContinue()

    def statsReset():
        if confirm(output.notify(f"Are you sure?", Print= False)):
            resetDATA(YAML, 'RockPaperScissors')
            clear()
            output.success(f"All done, good as new.")
            back()
        else:
            clear()
            output.error(f"Okay then.")
            back()

    print()
    output.stamp(f"Welcome to RockPaperScissors!")
    output.note(1, YAML['Settings']['Prefix'])
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

        YAML['RockPaperScissors']['P1']['LastChoice']  = p1['input']
        YAML['RockPaperScissors']['CPU']['LastChoice'] = cpu['input']
        YAML['RockPaperScissors']['LastWinner']        = winner['name']
        writeYAML()

        if winner == p1:
            YAML['RockPaperScissors']['P1']['Wins'] += 1
        if winner == cpu:
            YAML['RockPaperScissors']['CPU']['Wins'] += 1
        if winner == pN:
            YAML['RockPaperScissors']['Ties'] += 1
        writeYAML()

        back()

    elif choice == "2" or choice.casefold() == "duo":
        rps.duoMode()

        pN = rps.pN
        p1 = rps.p1
        p2 = rps.p2
        winner = rps.winner

        YAML['RockPaperScissors']['P1']['LastChoice'] = p1['input']
        YAML['RockPaperScissors']['P2']['LastChoice'] = p2['input']
        YAML['RockPaperScissors']['LastWinner']       = winner['name']
        writeYAML()

        if winner == p1:
            YAML['RockPaperScissors']['P1']['Wins'] += 1
        if winner == p2:
            YAML['RockPaperScissors']['P2']['Wins'] += 1
        if winner == pN:
            YAML['RockPaperScissors']['Ties'] += 1
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
        output.note(1, YAML['Settings']['Prefix'])
        print()
        output.option(1, "Start Game")
        output.option(2, "Difficulty: " + X0.LETTUCE + YAML['TicTacToe']['Difficulty'])
        output.option(0, "Back")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        result = None

        if choice == "1":
            clear()
            print()
            output.notify("Game mode...")
            output.note(1, YAML['Settings']['Prefix'])
            print()
            output.option(1, "Solo")
            output.option(2, "Duo")
            output.option(0, "Back")
            choice = intake.prompt()
            choice = choiceCheck(choice)
            if choice == "1":
                result = ttt.soloMode(YAML['TicTacToe']['Difficulty'])
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
            output.note(1, YAML['Settings']['Prefix'])
            output.note(f"Current is {X0.LETTUCE}{YAML['TicTacToe']['Difficulty']}{C0.END}")
            print()
            allowed = "HME123"
            choice = intake.prompt()
            choice = choiceCheck(choice)
            if goThro(choice.upper(), allowed) and len(choice) == 1:
                if choice == "1": choice = "H"
                if choice == "2": choice = "M"
                if choice == "3": choice = "E"
                YAML['TicTacToe']['Difficulty'] = choice.upper()
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
        print(f" {X0.YELLOW}-{C0.END} " + f"X Wins     : {X0.GRAY}{YAML['TicTacToe']['xWins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"O Wins     : {X0.GRAY}{YAML['TicTacToe']['oWins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Ties       : {X0.GRAY}{YAML['TicTacToe']['Ties']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last Winner: {X0.GRAY}{YAML['TicTacToe']['LastWinner']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last Board :-\n")
        print(ttt.displayBoard(YAML['TicTacToe']['LastBoard'], True, left=f' {X0.YELLOW}-{C0.END} '))
        enterContinue()

    def statsReset():
        if confirm(output.notify(f"Are you sure?", Print= False)):
            resetDATA(YAML, 'TicTacToe')
            clear()
            output.success(f"All done, good as new.")
            back()
        else:
            clear()
            output.error(f"Okay then.")
            back()

    print()
    output.stamp(f"Welcome to TicTacToe!")
    output.note(1, YAML['Settings']['Prefix'])
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

            YAML['TicTacToe']['LastWinner'] = winner['name']
            YAML['TicTacToe']['LastBoard'] = board

            if winner == ttt.s.x:
                YAML['TicTacToe']['xWins'] = int(YAML['TicTacToe']['xWins']) + 1
            if winner == ttt.s.o:
                YAML['TicTacToe']['oWins'] = int(YAML['TicTacToe']['oWins']) + 1
            if winner == ttt.tied:
                YAML['TicTacToe']['Ties'] = int(YAML['TicTacToe']['Ties']) + 1
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
    updateWindow(f"msp")

    def mspConfMenu():
        global mspConfSubMenu
        mspConfSubMenu = mspConfMenu
        updateWindow("mspConfSub")

        print()
        output.stamp("Minesweeper Config:")
        output.note(1, YAML['Settings']['Prefix'])
        print()
        output.option(1, "Map Size: " + X0.LETTUCE + str(YAML['Minesweeper']['Dimension']) + C0.END)
        output.option(2, "Bomb Count: " + X0.LETTUCE + str(YAML['Minesweeper']['BombCount']) + C0.END)
        output.option(0, "Back")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        if choice == "1":
            clear()
            print()
            output.stamp("What do you want the map size to be?")
            output.note(1, YAML['Settings']['Prefix'])
            output.note(f"Map size ranges from {X0.YELLOW}1:99{C0.END}")
            output.note(f"I don't recommend anything above 25 for your machine's health, also I do not recommend anything above 10 for the looks of it.")
            output.note(f"Current is {X0.LETTUCE}{YAML['Minesweeper']['Dimension']}{C0.END}")
            print()

            choice = intake.prompt()
            choice = choiceCheck(choice)

            allowed = "0123456789"
            if goThro(choice, allowed):
                choice = int(choice)
                if 99 >= choice > 0:
                    YAML['Minesweeper']['Dimension'] = choice
                    writeYAML()
                    clear()
                    output.success("Changes saved.")
                    back()

        if choice == "2":
            clear()
            print()
            output.stamp("How many bombs do you want there to be?")
            output.note(1, YAML['Settings']['Prefix'])
            output.note(f"Bombs count ranges from {X0.YELLOW}1:{YAML['Minesweeper']['Dimension']**2}{X0.END}")
            output.note(f"Current is {X0.LETTUCE}{YAML['Minesweeper']['BombCount']}{C0.END}")
            print()

            choice = intake.prompt()
            choice = choiceCheck(choice)

            allowed = "0123456789"
            if goThro(choice, allowed):
                choice = int(choice)
                if (YAML['Minesweeper']['Dimension']**2) >= choice > 0:
                    YAML['Minesweeper']['BombCount'] = choice
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
        print(f" {X0.YELLOW}-{C0.END} " + f"Total Wins :     {X0.GRAY}{YAML['Minesweeper']['Wins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total Loses:     {X0.GRAY}{YAML['Minesweeper']['Defeats']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total Dug Spots: {X0.GRAY}{YAML['Minesweeper']['SpotsDug']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last Map:-")
        #print(f" {x.YELLOW}-{c.END} " + f": {x.GRAY}{apps['msp']['']}{c.END}")

        BIN['Minesweeper'].print(True)

        enterContinue()

    def statsReset():
        if confirm(output.notify(f"Are you sure?", Print= False)):
            resetDATA(YAML, 'Minesweeper')
            resetDATA(BIN,  'Minesweeper')
            clear()
            output.success(f"All done, good as new.")
            back()
        else:
            clear()
            output.error(f"Okay then.")
            back()

    print()
    output.stamp(f"Welcome to Minesweeper!")
    output.note(1, YAML['Settings']['Prefix'])
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
        dim   = YAML['Minesweeper']['Dimension']
        bombC = YAML['Minesweeper']['BombCount']
        msp.startGame( SIZE = dim, BOMBS = bombC )

        if msp.gameWon:
            YAML['Minesweeper']['Wins']  += 1
        else:
            YAML['Minesweeper']['Defeats'] += 1

        YAML['Minesweeper']['SpotsDug'] += len(msp.BD.playerDug)
        BIN['Minesweeper'] = msp.BD

        writeYAML()
        writeBINARY()
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
        output.note(1, YAML['Settings']['Prefix'])
        print()
        output.option(1, "Hit on Soft 17: " + (f"{X0.LETTUCE}Yes" if YAML['Blackjack']['Soft17'] else f"{X0.RED}No") + C0.END)
        output.option(0, "Back")

        choice = intake.prompt()
        choice = choiceCheck(choice)
        
        if choice == "1":
            clear()
            output.stamp("Hit on Soft 17? " + f"{X0.GRAY}({X0.LETTUCE}Y{X0.GRAY},{X0.RED}N{X0.GRAY})")
            output.note(1, YAML['Settings']['Prefix'])
            output.note(f"To explain, this option is to either make the dealer hit on 17 or not.")
            output.note(f"")
            output.note(f"Current is {(f'{X0.LETTUCE}Yes' if YAML['Blackjack']['Soft17'] else f'{X0.RED}No')}")

            choice = intake.prompt()
            choice = choiceCheck(choice)

            if goThro(choice, "YNyn12"):
                if choice.upper() in ("Y", "1"):
                    YAML['Blackjack']['Soft17'] = True
                if choice.upper() in ("N", "2"):
                    YAML['Blackjack']['Soft17'] = False
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
            resetDATA(YAML, 'Blackjack')
            clear()
            output.success(f"All done, good as new.")
            back()
        else:
            clear()
            output.error(f"Okay then.")
            back()

    print()
    output.stamp("Welcome to BlackJack!")
    output.note(1, YAML['Settings']['Prefix'])
    output.note(f"Current Balance is {X0.LETTUCE}{YAML['Blackjack']['Balance']}C")
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
        result    = bjk.startGame(YAML['Blackjack']['Balance'], 1, YAML['Blackjack']['Soft17'])

        YAML['Blackjack']['Balance']  = result[0]
        YAML['Blackjack']['LastBet'] = result[1]

        writeYAML()

        back()

    elif choice == "2":

        available = YAML['Blackjack']['Reward'] != today
        clear()

        print()
        output.stamp(f"Bienvenue à la Banque de {X0.LETTUCE}SPAIME²{X0.VIOLET}!")
        output.note(1, YAML['Settings']['Prefix'])
        output.note("Reward " + ((f"{X0.LETTUCE}available") if available else (f"{X0.RED}not available")) + f"{X0.GRAY}.")
        print()
        output.option(1, (C0.STRIKE if not available else "") + "Claim Daily")
        output.option(2, "Debt")
        output.option(0, "Back")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        if choice == "1" and available:
            clear() 

            YAML['Blackjack']['Reward'] = today
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
                YAML['Blackjack']['Balance'] += reward
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
    updateWindow(f"sdk")

    def sdkConfMenu():
        global sdkConfSubMenu
        sdkConfSubMenu = sdkConfMenu
        updateWindow("sdkConfSub")

        print()
        output.stamp("Sudoku Config:")
        output.note(1, YAML['Settings']['Prefix'])
        print()
        output.option(1, f"Empty Spots: {X0.LETTUCE}{YAML['Sudoku']['Empty']}{C0.END}")
        output.option(0, f"Back")

        choice = intake.prompt()
        choice = choiceCheck(choice)
        
        if choice == "1":
            clear()
            output.stamp("How many empty spots do you want?!")
            output.note(1, YAML['Settings']['Prefix'])
            output.note(f"Current is {X0.LETTUCE}{YAML['Sudoku']['Empty']}")

            choice = intake.prompt()
            choice = choiceCheck(choice)

            if goThro(choice, "0123456789"):
                choice = int(choice)

                if 81 >= choice > 0:
                    YAML['Sudoku']['Empty'] = choice

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
        print(f" {X0.YELLOW}-{C0.END} " + f"Total Wins :     {X0.GRAY}{YAML['Sudoku']['Wins']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Total Validations: {X0.GRAY}{YAML['Sudoku']['Validated']}{C0.END}")
        print(f" {X0.YELLOW}-{C0.END} " + f"Last Puzzle:-")

        BIN['Sudoku'].print(D=False)

        enterContinue()

    def statsReset():
        if confirm(output.notify(f"Are you sure?", Print= False)):
            resetDATA(YAML, 'Sudoku')
            resetDATA(BIN,  'Sudoku')
            clear()
            output.success(f"All done, good as new.")
            back()
        else:
            clear()
            output.error(f"Okay then.")
            back()

    print()
    output.stamp("Welcome to Sudoku!")
    output.note(1, YAML['Settings']['Prefix'])
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
        sdk.startGame(YAML['Sudoku']['Empty'], YAML['Settings']['Prefix'], BIN['Sudoku'])

        BIN['Sudoku']                    = sdk.sudoku
        YAML['Sudoku']['Wins']     += 1 if sdk.gameWon else 0
        YAML['Sudoku']['Validated'] = sdk.sudoku.timesVal

        writeYAML()
        writeBINARY()
        back()
    elif choice == "2":
        clear()
        sdk.startGame(YAML['Sudoku']['Empty'], YAML['Settings']['Prefix'])

        BIN['Sudoku']                    = sdk.sudoku
        YAML['Sudoku']['Wins']     += 1 if sdk.gameWon else 0
        YAML['Sudoku']['Validated'] = sdk.sudoku.timesVal

        writeYAML()
        writeBINARY()
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
    output.note(1, YAML['Settings']['Prefix'])
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
        bfi.startApp('V')

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
        YAML['Settings']['Name'] = str(name)
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

            YAML['Settings']['Sex'] = sex

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
        age_old = YAML['Settings']['Age']
        try:
            YAML['Settings']['Age'] = int(age)
        except:
            clear()
            output.error(f"Please input numbers only.")
        else:
            if (YAML['Settings']['Age'] >= 100 or YAML['Settings']['Age'] < 0) and not (isAdmin()):
                clear()
                output.error(f"How tf can you be {YAML['Settings']['Age']} years-old?")
                output.error(f"I'll return it to {age_old}.")
                YAML['Settings']['Age'] = age_old
                return
            try:
                writeYAML()
            except:
                clear()
                output.error(f"Something went wrong.")
            else:
                writeYAML()
                clear()
                if YAML['Settings']['Age'] == 69:
                    output.success(f"Nice.")
                else:
                    output.success(f"Changes saved.")

    def prefix_change(thing):
        clear()
        YAML['Settings']['Prefix'] = thing
        writeYAML()

    print()
    output.stamp(f"Options:")
    output.note(1, YAML['Settings']['Prefix'])
    print()
    output.option(1, f"Name: {X0.GREEN}{YAML['Settings']['Name'] if YAML['Settings']['Name'] != '' else 'N/A'}")
    output.option(2, f"Gender: {X0.GREEN}{YAML['Settings']['Sex'] if YAML['Settings']['Sex'] != None else 'N/A'}")
    output.option(3, f"Age: {X0.GREEN}{YAML['Settings']['Age']}")
    output.option(4, f"Prefix: {X0.GREEN}{YAML['Settings']['Prefix']}")
    output.option(8, f"Rest Games' Stats")
    output.option(9, f"Rest Application")
    output.option(0, f"Home")

    choice = intake.prompt()
    choice = choiceCheck(choice)

    if choice == "1" or choice.casefold() == "name":

        clear()
        print()
        output.stamp(f"What do you wanna be called?")
        output.note(1, YAML['Settings']['Prefix'])
        output.note(f"Current is {X0.GREEN}{YAML['Settings']['Name'] if YAML['Settings']['Name'] != '' else 'N/A'}")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        nameChange(choice)

        back()

    elif choice == "3" or choice.casefold() == "age":

        clear()
        print()
        output.stamp(f"How old are you?")
        output.note(1, YAML['Settings']['Prefix'])
        output.note(f"Current is {X0.GREEN}{YAML['Settings']['Age']}")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        ageChange(choice)

        back()
    elif choice == "2" or choice.casefold() == "gender":

        clear()
        print()
        output.stamp(f"Cation, Anion or Zwitterion? {X0.LETTUCE}(M,F,N)")
        output.note(1, YAML['Settings']['Prefix'])
        output.note(f"Current is {X0.GREEN}{YAML['Settings']['Sex'] if YAML['Settings']['Sex'] != None else 'N/A'}")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        sexChange(choice)

        back()
    elif choice == "4" or choice.casefold() == "prefix":

        clear()
        print()
        output.stamp(f"Set prefix to what?")
        output.note(1, YAML['Settings']['Prefix'])
        output.note(f"Current is {X0.GREEN}{YAML['Settings']['Prefix']}")

        choice = intake.prompt()
        choice = choiceCheck(choice)

        prefix_change(choice)

        back()
    elif choice == "8" or choice.casefold() == "reset stats":

        clear()
        output.notify(f"Continuing would mean you want to reset statistics to default.")
        if confirm(output.notify(f"Are you sure?", Print=False)):
            print()
            output.notify(f"Please type {X0.GRAY}{C0.ITALIC}\"{X0.LETTUCE}{YAML['Settings']['Prefix']}reset{X0.GRAY}\"{C0.END}{X0.GRAY} to further confirm.")

            choice = intake.prompt()
            choice = choiceCheck(choice)

            if choice == f"{YAML['Settings']['Prefix']}reset":
                resetDATA(YAML)
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
            output.notify(f"Please type {X0.GRAY}{C0.ITALIC}\"{X0.LETTUCE}{YAML['Settings']['Prefix']}reset{X0.GRAY}\"{C0.END}{X0.GRAY} to further confirm.")

            choice = intake.prompt()
            choice = choiceCheck(choice)

            if choice == f"{YAML['Settings']['Prefix']}reset":
                resetDATA()
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
    print(f" {X0.YELLOW}-{C0.END} {YAML['Settings']['Prefix']}" + f"help [┬]   : {X0.GRAY}Shows this menu.{C0.END}")
    print(                                          f"          ├math: {X0.GRAY}Shows help about Math & Logic.{C0.END}")
    print(                                          f"          ├rnd : {X0.GRAY}Shows help about Randomeur.{C0.END}")
    print(                                          f"          ├rps : {X0.GRAY}Shows help about RockPaperScissors.{C0.END}")
    print(                                          f"          ├ttt : {X0.GRAY}Shows help about TicTacToe.{C0.END}")
    print(                                          f"          ├msp : {X0.GRAY}Shows help about Minesweeper.{C0.END}")
    print(                                          f"          └bjk : {X0.GRAY}Shows help about BlackJack.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {YAML['Settings']['Prefix']}" + f"back:        {X0.GRAY}Returns you a page back.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {YAML['Settings']['Prefix']}" + f"home:        {X0.GRAY}Returns you to home page.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {YAML['Settings']['Prefix']}" + f"refr:        {X0.GRAY}Refreshes current page.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {YAML['Settings']['Prefix']}" + f"exit:        {X0.GRAY}To safely exit the app.{C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {YAML['Settings']['Prefix']}" + f"dev1:        {X0.GRAY}Enters eval() mode. {X0.RED}{C0.DIM}(dev-only){C0.END}")
    print(f" {X0.YELLOW}-{C0.END} {YAML['Settings']['Prefix']}" + f"dev2:        {X0.GRAY}Enters exec() mode. {X0.RED}{C0.DIM}(dev-only){C0.END}")
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
    with open('./extras/logo.txt', 'r') as file:
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
    if YAML['Settings']['Name'] == '':
        output.notify(f"Bye-bye{X0.VIOLET}!")
    else:
        output.notify(f"Bye-bye, {X0.GREEN}{YAML['Settings']['Name']}{X0.VIOLET}!")

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

    if YAML['Settings']['FirstTime']:
        YAML['Settings']['FirstTime'] = False
        writeYAML()
        infoF()

    mainMenu()
    clear()

#==================================================================#
