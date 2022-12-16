import sys
from os.path import abspath, dirname, join

# Sets path to the app's main folder
if __name__ == "__main__":
    sys.path.insert(0, abspath(join(dirname(__file__), '../..')))

from scripts.libs import *



def addHP(this, num):
    print(f"{this.name} healed {num} ♥.")
    this.health += num


def remHP(this, num):
    print(f"{this.name} was damaged {num} ♥.")
    this.health -= num

# Funky Constants:
TYPES:list = ['Creature', 'Block', 'Item', 'Other']

ITEMS:dict    = {}
CATEGORY:list = ['Weapon', 'Consumable']

SPIKES = '☼'

SQUARE = {'W': '□',
          'B': '■',
          'P': '▣'}

HEART  = {'W': '♡',
          'B': '♥'}

STAR   = {'W': '☆',
          'B': '★'}

FLAG   = {'W': '⚐',
          'B': '⚑'}

# Things Definition:
class Thing:

    def isMoveable(this):
        try: this.position and this.world
        except: return False
        return True

    def move(this, X, Y):
        if this.isMoveable():
            maxX, maxY = (len(this.world.map), ) * 2
            x   , y    = this.position[0], this.position[1]
            X   , Y    = X % maxX, Y % maxY

            this.position = [X, Y]

            this.world.map[x][y][this.type].remove(this)
            this.world.map[X][Y][this.type].append(this)

    def go(this, direction:str, amount:int = 1) -> int:
        if this.isMoveable():
            x, y = this.position[0], this.position[1]

            if direction.upper() == '+X': this.move(x+1,y)
            if direction.upper() == '-X': this.move(x-1,y)
            if direction.upper() == '+Y': this.move(x,y+1)
            if direction.upper() == '-Y': this.move(x,y-1)

    def distance(this, Obj):
        if this.isMoveable():
            X, Y = this.position[0], this.position[1]
            x, y = Obj.position [0], Obj.position [1]

            distance = ((X - x) ** 2 + ( Y - y) ** 2 ) ** 0.5

            return distance
        else:
            return 'unidentified'





# Items Definition:

class Item(Thing):
    def __init__(this, name:str, id:int, category:str, func:dict, attributes:dict = {}) -> None:
        this.name      = name
        this.id        = id
        this.category  = category
        this.func      = func
        this.attrs     = attributes
        this.type      = 'Item'
        ITEMS[id]      = this



class Apple(Item):
    def __init__(this,

                name     = 'Apple',
                id       = 'apple',
                func     = {addHP: [10]},
                attributes: dict = {}) -> None:

        super().__init__(name, id, 'Consumable', func, attributes)


class Poison(Item):
    def __init__(this,

                name     = 'Poison',
                id       = 'poison',
                func     = {remHP: [10]},
                attributes: dict = {}) -> None:

        super().__init__(name, id, 'Consumable', func, attributes)




# Blocks Definition:
BLOCKS:dict = {}

class Block(Item, Thing):
    def __init__(this, name: str, id: int, visuals:str, attributes:dict = {}) -> None:
        super().__init__(name, id, None, attributes)
        this.type  = 'Block'
        this.visuals = visuals
        BLOCKS[id] = this


# Races Definition:
RACES:dict = {}

class Race:
    def __init__(this, name:str, id:int|str, health:int, attack:int, inventory:list) -> None:
        this.name      = name
        this.health    = health
        this.attack    = attack
        this.inventory = inventory

        RACES[id]      = this


# Actually Defining shit

MAGE = Race(
    'Mage',
    'mage',
    80, 20,
    [Apple(name= 'Bad Apple',func={remHP: [5]})]
    )


GRASS      = Block('Grass'      , 0, X0.GREEN + SQUARE['B'] + C0.END)
STONE      = Block('Stone'      , 1, X0.GRAY  + SQUARE['B'] + C0.END)
BLOODSTONE = Block('Blood Stone', 2, X0.RED   + SQUARE['P'] + C0.END)


# World/Map Definition:
class World():

    def __init__(this, name:str, X:int, Y:int) -> None:
        this.name = name

        this.X    = X
        this.Y    = Y

        this.map  = this.makeMap()
        this.size = X * Y


    def __getitem__(this, X) -> list:
        return this.map[X]
    
    def setBlockTo(this, block:Block, pos1:list = (), pos2:list = ()):

        # If no positions were given
        # It'll just set the whole map to that block
        if pos1 == pos2 == list():

            # Going through every block to change
            for _x in range(len(this.map)):
                for _y in range(len(this.map[_x])):
                    this.map[_x][_y]['Block'] = block
                     
        # If only pos1 was given
        # It'll set only pos1 to that block
        if pos1 != pos2 == list():

            # Changing that single block
            this.map[pos1[0]][pos1[1]]['Block'] = block

        # If both positions were given:
        # It'll make a square of that block
        if pos1 != pos2 != list():

            # Getting the X range
            xMax = max(pos1[0], pos2[0])
            xMin = min(pos1[0], pos2[0])

            # Getting the Y range
            yMax = max(pos1[1], pos2[1])
            yMin = min(pos1[1], pos2[1])

            # Going though every block in range to change
            for _x in range(xMin, xMax+1):
                for _y in range(yMin, yMax+1):
                    this.map[_x][_y]['Block'] = block
         

    def makeMap(this):

        TILE  = {
            'Block'   : GRASS,
            'Creature': [],
            'Item'    : [],
            'Others'  : []
            }

        MAP   = [[copy.deepcopy(TILE) for _ in range(this.Y)] for _ in range(this.X)]
        return MAP


    def addTo(this, obj:Thing, x:int, y:int):
        objType = obj.type

        this.map[x][y][objType].append(obj)

    def print(this):

        for line in this.map:
            for spot in line:
                if spot['Creature'] == []:
                    print(spot['Block'].visuals, end=' ')
                else:
                    print(spot['Creature'][-1].visuals, end=' ')
            print()
        print()

        



# Characters Definition:
class Creature(Thing):

    def __init__(this, name:str, race:Race, visuals:str, world:World, position:list = [0,0]) -> None:
        this.name      = name
        this.type      = 'Creature'
        this.race      = race
        this.visuals   = visuals

        this.world     = world
        this.position  = list(position)
        world.addTo(this, *position)

        this.attack    = race.attack
        this.health    = race.health
        this.maxHealth = race.health

        this.inventory:list = race.inventory


    def __str__(this) -> str:
        inventory = [_.name for _ in (this.inventory)]

        return f"""
        {X0.END}=====[{X0.GOLD}Character List{X0.END}]=====
        {X0.VIOLET}Name: {this.name}
        {X0.VIOLET}World: {this.world.name}
        {X0.VIOLET}Position: {this.position[0]}, {this.position[1]}
        {X0.VIOLET}Race: {this.race.name}
        {X0.VIOLET}Health: {this.health}/{this.maxHealth} {X0.RED}♥
        {X0.VIOLET}Inventory: {', '.join(inventory)}
        {X0.END}==========================
        """.replace(' '*8, '').replace(':', X0.GRAY + ':')


    def hit(this, who) -> int:
        print(f"{this.name} hit {who.name} with {this.attack} ♥.")
        who.health -= this.attack


    def use(this, item:Item, who:Thing = None) -> None:

        who = this if who == None else who

        if item in this.inventory:
            print(f"{this.name} used {item.name}.")
            for Use in item.func:
                args = item.func[Use]
                Use(who, *args)
            this.inventory.remove(item)
        else:
            print(f"Item {item.name} not available.")



if __name__ == '__main__':

    clear()

    hell    = World('Hell', 20, 20)
    fastre  = Creature('Fastre', MAGE, X0.VIOLET + FLAG['B'] + C0.END, hell, (0,0))
    slowre  = Creature('Slowre', MAGE, X0.GOLD   + FLAG['W'] + C0.END, hell, (5,5))

    print(fastre, slowre)
    hell.setBlockTo(BLOODSTONE, [10,00], [19,19])


    while True:

        from pynput import keyboard
        from pynput.keyboard import Key
        def on_press(key):
            print(key)
            try:
                if key  == Key.esc: sys.exit(0)
                if key.char == 'w': fastre.go('-x')
                if key.char == 's': fastre.go('+x')
                if key.char == 'a': fastre.go('-y')
                if key.char == 'd': fastre.go('+y')
            finally:
                return False

        # Collect events until released
        with keyboard.Listener(on_press=on_press) as listener:
            clear()
            hell.print()
            print(fastre)
            listener.join()