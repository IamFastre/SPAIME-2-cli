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



# Things Definition:
class Thing:

    def isMoveable(this):
        try: this.position and this.world
        except: return False
        return True

    def move(this, X, Y):
        if this.isMoveable():
            x, y = this.position[0], this.position[1]

            this.position = (X, Y)
            this.world.map[x][y][this.type].remove(this)
            this.world.map[X][Y][this.type].append(this)

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
    def __init__(this, name: str, id: int, func:dict, attributes:dict = {}) -> None:
        super().__init__(name, id, func, attributes)
        this.type  = 'Block'
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

MAGE = Race(
    'Mage',
    'mage',
    80, 20,
    [Apple(name= 'Bad Apple',func={remHP: [5]})]
    )




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


    def makeMap(this):

        TILE  = {
            'Block'   : [],
            'Creature': [],
            'Item'    : [],
            'Others'  : []
            }

        MAP   = [[copy.deepcopy(TILE) for _ in range(this.Y)] for _ in range(this.X)]
        return MAP


    def addTo(this, obj:Thing, x:int, y:int):
        objType = obj.type

        this.map[x][y][objType].append(obj) 

        



# Characters Definition:
class Creature(Thing):

    def __init__(this, name:str, race:Race, world:World, position:tuple = (0,0)) -> None:
        this.name      = name
        this.type      = 'Creature'
        this.race      = race

        this.world     = world
        this.position  = position
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

    hell    = World('Hell', 10, 10)
    fastre  = Creature('Fastre', MAGE, hell, (0,0))
    slowre  = Creature('Slowre', MAGE, hell, (5,5))

    print(fastre, slowre)